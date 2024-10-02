import os
import os.path
import pathlib
import itertools

from flask import Flask, jsonify, render_template, redirect, request, url_for, send_from_directory, current_app, \
    send_file
from werkzeug.utils import secure_filename

from bozzaCommissione import bozzaCommissione
from longest_list import longest_list
from script_commissioni_csv import script_commissioni_csv
from script_commissioni_xlsx import script_commissioni_xlsx
from script_laureandi_csv import script_laureandi_csv
from script_laureandi_xlsx import script_laureandi_xlsx
from slot_temporali import slot_temporali

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.jinja_env.filters['zip_longest'] = itertools.zip_longest

NUMERO_SLOT = 8


@app.route('/', methods=["GET", "POST"])
def main():
    error = None
    if request.method == 'POST':
        # controllo momentaneo per l'accesso alla piattaforma
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('upload_file', nomeFile="", n_disp=NUMERO_SLOT))
    return render_template('main.html', error=error)


# viene specificato il path dove salvare i file caricati e da scaricare

FILE_UPLOADS_LAUREANDI = os.path.dirname(os.path.abspath(__file__)) + '/static/files/uploads/laureandi/'
app.config['FILE_UPLOADS_LAUREANDI'] = FILE_UPLOADS_LAUREANDI
FILE_UPLOADS_COMMISSARI = os.path.dirname(os.path.abspath(__file__)) + '/static/files/uploads/commissari/'
app.config['FILE_UPLOADS_COMMISSARI'] = FILE_UPLOADS_COMMISSARI
FILE_DOWNLOADS = os.path.dirname(os.path.abspath(__file__)) + '/static/files/downloads/'
app.config['FILE_DOWNLOADS'] = FILE_DOWNLOADS

# vengono specificati i formati ammessi da caricare
app.config["ALLOWED_FILE_EXTENSIONS"] = ["CSV", "XLSX"]


# controllo che l'estensione del file caricato sia ammesso
def allowed_file(filename):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False




@app.route('/upload', methods=["GET"])
def upload_file():
    countc = 0
    for path in pathlib.Path(FILE_UPLOADS_COMMISSARI).iterdir():

        if path.is_file():
            countc += 1

    existc = countc > 0
    countl = 0
    for path in pathlib.Path(FILE_UPLOADS_LAUREANDI).iterdir():

        if path.is_file():
            countl += 1

    existl = countl > 0
    return render_template("upload_file.html", title='file upload',
                           nomeFile="", segnatoL=existl, segnatoP=existc, n_disp=NUMERO_SLOT)


@app.route('/upload_laureandi', methods=["POST"])
def upload_file_laureandi():
    if request.files:

        file = request.files["myfilel"]

        # controllo della validità del file caricato

        if file.filename == "":
            print("Image must have a filename")
            return redirect(request.url)

        if not allowed_file(file.filename):
            print("That file extension is not allowed")
            return redirect(request.url)

        else:
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['FILE_UPLOADS_LAUREANDI'], filename))

            # una volta controllata l'estensione del file si controlla quale file sia (laureandi o dispoComm)
            # per capire quale operazione vada fatta
            countc = 0
            for path in pathlib.Path(FILE_UPLOADS_COMMISSARI).iterdir():

                if path.is_file():
                    countc += 1

            existc = countc > 0
            countl = 0
            for path in pathlib.Path(FILE_UPLOADS_LAUREANDI).iterdir():

                if path.is_file():
                    countl += 1

            existl = countl > 0
            return render_template("upload_file.html", title='file upload',
                                   nomeFile="", segnatoL=existl, segnatoP=existc, n_disp=NUMERO_SLOT)

    return render_template("upload_file.html", title='file upload', n_disp=NUMERO_SLOT)


@app.route('/upload_commissari', methods=["POST"])
def upload_file_commissari():
    global NUMERO_SLOT
    if request.files:

        file = request.files["myfilec"]

        # controllo della validità del file caricato

        if file.filename == "":
            print("Image must have a filename")
            return redirect(request.url)

        if not allowed_file(file.filename):
            print("That file extension is not allowed")
            return redirect(request.url)

        else:
            NUMERO_SLOT = int(request.form["n_disponibilita"])
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['FILE_UPLOADS_COMMISSARI'], filename))

            # una volta controllata l'estensione del file si controlla quale file sia (laureandi o dispoComm)
            # per capire quale operazione vada fatta
            countc = 0
            for path in pathlib.Path(FILE_UPLOADS_COMMISSARI).iterdir():

                if path.is_file():
                    countc += 1

            existc = countc > 0
            countl = 0
            for path in pathlib.Path(FILE_UPLOADS_LAUREANDI).iterdir():

                if path.is_file():
                    countl += 1

            existl = countl > 0
            return render_template("upload_file.html", title='file upload',
                                   nomeFile="", segnatoL=existl, segnatoP=existc, n_disp=NUMERO_SLOT)


# applicazione che richiama lo script per il file relativo ai laureandi nel caso sia nel formato csv

@app.route('/laureandi', methods=["GET", "POST"])
def laureandi():
    # si sceglie quale applicazione di scripting lanciare a seconda della tipologia di file caricato dall'utente
    try:
        lau = script_laureandi_csv(FILE_UPLOADS_LAUREANDI)
    except (FileNotFoundError, IsADirectoryError) as e:
        try:
            lau = script_laureandi_xlsx(FILE_UPLOADS_LAUREANDI)
        except (FileNotFoundError, IsADirectoryError) as e:
            return render_template("upload_file.html", title='file upload', n_disp=NUMERO_SLOT)
    if lau is not None:
        if request.method == "POST":
            tri = int(request.form['commissioniTriennali'])
            mag = int(request.form['commissioniMagistrali'])
            try:
                comm = script_commissioni_csv(FILE_UPLOADS_COMMISSARI, NUMERO_SLOT)
            except (FileNotFoundError, IsADirectoryError) as e:
                try:
                    comm = script_commissioni_xlsx(FILE_UPLOADS_COMMISSARI, NUMERO_SLOT)
                except (FileNotFoundError, IsADirectoryError) as e:
                    return render_template("upload_file.html", title='file upload', n_disp=NUMERO_SLOT)
            lettere = slot_temporali(NUMERO_SLOT)
            long = longest_list(lau.get('relatori_tri'), lau.get('relatori_mag'), comm)
            # vengono restituite le informazioni relative al numero dei laureandi e al numero di commissioni
            # tenendo conto delle eventuali modifiche effettuate al numero di commissioni
            return render_template("commissioni.html", title='commissioni', dispComm=comm,
                                   prof_t=lau.get('relatori_tri'), prof_m=lau.get('relatori_mag'),
                                   comm_m=mag, comm_t=tri, lettere=lettere, lunghezza_max=long)
        else:
            tri = lau.get('commissioni_t')
            mag = lau.get('commissioni_m')

        return render_template("laureandi.html", title='info', lt=lau.get('lau_triennale'),
                               ct=tri, lm=lau.get('lau_magistrale'), cm=mag)


@app.route('/commissioni', methods=["GET", "POST"])
def commissioni():

    # si sceglie quale applicazione di scripting lanciare a seconda della tipologia di file caricato dall'utente
    try:
        comm = script_commissioni_csv(FILE_UPLOADS_COMMISSARI, NUMERO_SLOT)
        try:
            lau = script_laureandi_csv(FILE_UPLOADS_LAUREANDI)
        except (FileNotFoundError, IsADirectoryError) as e:
            try:
                lau = script_laureandi_xlsx(FILE_UPLOADS_LAUREANDI)
            except (FileNotFoundError, IsADirectoryError) as e:
                return render_template("upload_file.html", title='file upload', n_disp=NUMERO_SLOT)
        lettere = slot_temporali(NUMERO_SLOT)
        long = longest_list(lau.get('relatori_tri'), lau.get('relatori_mag'), comm)
    except (FileNotFoundError, IsADirectoryError) as e:
        try:
            comm = script_commissioni_xlsx(FILE_UPLOADS_COMMISSARI, NUMERO_SLOT)
        except (FileNotFoundError, IsADirectoryError) as e:
            return render_template("upload_file.html", title='file upload')
        try:
            lau = script_laureandi_csv(FILE_UPLOADS_LAUREANDI)
        except FileNotFoundError or IsADirectoryError:
            try:
                lau = script_laureandi_xlsx(FILE_UPLOADS_LAUREANDI)
            except (FileNotFoundError, IsADirectoryError) as e:
                return render_template("upload_file.html", title='file upload')
        lettere = slot_temporali(NUMERO_SLOT)
        long = longest_list(lau.get('relatori_tri'), lau.get('relatori_mag'), comm)
    return render_template("commissioni.html", title='commissioni', dispComm=comm,
                           prof_t=lau.get('relatori_tri'), prof_m=lau.get('relatori_mag'),
                           comm_m=lau.get('commissioni_m'), comm_t=lau.get('commissioni_t'),
                           lettere=lettere, lunghezza_max=long)


@app.route('/save', methods=["GET", "POST"])
def save():
    new_dict_flask = request.json
    try:
        comm = script_commissioni_csv(FILE_UPLOADS_COMMISSARI, NUMERO_SLOT)
    except FileNotFoundError:
        comm = script_commissioni_xlsx(FILE_UPLOADS_COMMISSARI, NUMERO_SLOT)
    if new_dict_flask is not None:
        bozzaCommissione(new_dict_flask[0], new_dict_flask[1], new_dict_flask[2], new_dict_flask[3], new_dict_flask[4],
                         app.config['FILE_DOWNLOADS'], NUMERO_SLOT)
    return redirect(request.url)


@app.route('/download', methods=["GET", "POST"])
def download():
    # vengono eliminati i file caricati per non avere precedenti quando si riapre l'applicazione
    filestoremove = [os.path.join(FILE_UPLOADS_COMMISSARI, f) for f in os.listdir(FILE_UPLOADS_COMMISSARI)]
    for f in filestoremove:
        os.remove(f)
    filestoremove = [os.path.join(FILE_UPLOADS_LAUREANDI, f) for f in os.listdir(FILE_UPLOADS_LAUREANDI)]
    for f in filestoremove:
        os.remove(f)

    return send_file('static/files/downloads/commissioni.xlsx', as_attachment=True)


@app.route('/delete', methods=["GET", "POST"])
def delete():
    # vengono eliminati i file caricati per non avere precedenti quando si riapre l'applicazione
    filestoremove = [os.path.join(FILE_UPLOADS_COMMISSARI, f) for f in os.listdir(FILE_UPLOADS_COMMISSARI)]
    for f in filestoremove:
        os.remove(f)
    filestoremove = [os.path.join(FILE_UPLOADS_LAUREANDI, f) for f in os.listdir(FILE_UPLOADS_LAUREANDI)]
    for f in filestoremove:
        os.remove(f)
    filestoremove = [os.path.join(FILE_DOWNLOADS, f) for f in os.listdir(FILE_DOWNLOADS)]
    for f in filestoremove:
        os.remove(f)
    return render_template("upload_file.html", title='file upload')


if __name__ == '__main__':
    app.run(debug=True)
