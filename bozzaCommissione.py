import xlsxwriter
import os
import copy
from string import ascii_uppercase
from script_commissioni_csv import script_commissioni_csv
from script_commissioni_xlsx import script_commissioni_xlsx
from slot_temporali import slot_temporali


def bozzaCommissione(disponibilita, numero_studenti, professori, supplenti, studprofnoncommissione, path, n_slot):
    name = "commissioni.xlsx"
    workbook = xlsxwriter.Workbook(path + name)

    # viene creata una copia del dizionario 'commissione' -> 'prof - nStudenti' presenti
    # che verrà poi usata per al creazione delle colonne dei supplenti
    copiaprof = copy.deepcopy(professori)

    # nel dizionario 'commissione' -> 'prof - nStudenti' viene isolato il nome del professore
    # eliminando il numero degli studenti
    for p in copiaprof:
        for k in range(len(copiaprof[p])):
            nome = copiaprof[p][k].split('-')
            copiaprof[p][k] = nome[0]

    # dizionario che comprende tutti i professori che non si trovano in nessuna commissione
    copiasupplenti = copy.deepcopy(supplenti)

    for i in disponibilita:
        for e in supplenti:
            if e in copiaprof[i] and e in copiasupplenti:
                del copiasupplenti[e]

    # lista che contiene la denominazione degli slot
    try:
        comm = script_commissioni_csv(os.path.dirname(os.path.abspath(__file__)) + '/static/files/uploads/commissari/',
                                      n_slot)
    except (FileNotFoundError, IsADirectoryError) as e:
        comm = script_commissioni_xlsx(os.path.dirname(os.path.abspath(__file__)) + '/static/files/uploads/commissari/',
                                       n_slot)
    lettere = slot_temporali(n_slot)

    # si itera nelle commissioni create
    num_caselle_disp = 0
    for i in disponibilita:
        numero_commissione = int(i[:1]) + 1
        # dato l'identificativo della commissione si sceglie se è triennale o magistrale
        if i[1:] == "tri":
            tipologia = "TRIENNALE "
        else:
            tipologia = "MAGISTRALE "
        # numero univoco per tipologia di commissione, crescente
        numero_commissione = str(numero_commissione)
        # viene creata una worksheet per ogni commissione
        worksheet = workbook.add_worksheet(tipologia + numero_commissione)
        worksheet.write(0, 0, "COMMISSIONE " + tipologia + numero_commissione)

        # numero di laureandi totali per la commissione corrente
        worksheet.write(2, 0, "NUMERO STUDENTI")
        ns = int(numero_studenti[i])
        worksheet.write(2, 1, ns)

        # si itera nella lista delle disponibilità della commissione corrente
        cond = True

        for j in range(len(lettere)):
            num_caselle_disp = str(num_caselle_disp)
            j = str(j)
            # viene data disponibilità nei giorni in cui tutti i professori nella commissione sono disponibili
            # e nei giorni in cui l'aula magna risulta prenotata
            if (disponibilita[i][j] == 'disp si' or disponibilita[i][j] == 'disp occupata') and cond:
                j = int(j)
                num_caselle_disp = int(num_caselle_disp) + 1
                worksheet.write(1, 0, "SLOT " + lettere[j])
                cond = False
                # si itera nella lista dei supplenti, si scelgono solo i professori che non sono presenti nella
                # commissione e che sono disponibili per quel giorno
                supplenticomm = ""
                for supp in supplenti:
                    # si controlla che il professore non sia nella commissione attuale
                    if supp not in copiaprof[i] and supp in comm:

                        # si controlla che il professore sia libero quel giorno
                        if supplenti[supp][j] == 'si' or supplenti[supp][j] == 'vuoto' or supplenti[supp][j] == 'ni':
                            # si controlla se il professore compare in altre commissioni
                            if supp in copiasupplenti:
                                # se il professore non compare in nessuna commissione viene messo un asterisco
                                supplenticomm = supplenticomm + supp + "*" + ", "
                            else:
                                # se è commissario in un altra commissione non compare niente
                                supplenticomm = supplenticomm + supp + ", "
                worksheet.write(5, 0, "SUPPLENTI")
                worksheet.write(5, 1, supplenticomm)

        # vengono scritti i nome dei commissari per la commissione corrente
        commissari = ""
        for p in copiaprof[i]:
            commissari = commissari + p + ", "
        worksheet.write(4, 0, "COMMISSIONE")
        worksheet.write(4, 1, commissari)

        worksheet.write(7, 0, "STUDENTI")
        # si itera nella lista dei professori associata alla commissione corrente
        # per associare ad ogni professore il numero degli studenti
        riga = 0
        for k in range(len(professori[i])):
            # viene tolto il trattino dal nome del professore
            nome_professore = professori[i][k].split('-')
            nomeprof = str(nome_professore[0])
            # si controlla se il professore ha laureandi
            if len(nome_professore) != 1:
                studenti = int(nome_professore[1])
                worksheet.write(8 + riga, 0, nomeprof)
                worksheet.write(8 + riga, 1, studenti)
                riga = riga + 1
        # si itera nella lista dei professori non in commissione ma che hanno laureandi in quella commissione
        # per associare ad ogni professore il numero dei propri studenti
        for k in range(len(studprofnoncommissione[i])):
            # viene tolto il trattino dal nome del professore
            nome_professore = studprofnoncommissione[i][k].split('-')
            nomeprof = str(nome_professore[0])
            # si controlla se il professore ha laureandi
            if len(nome_professore) != 1:
                studenti = int(nome_professore[1])
                worksheet.write(8 + riga, 0, nomeprof)
                worksheet.write(8 + riga, 1, studenti)
                riga = riga + 1

    workbook.close()
