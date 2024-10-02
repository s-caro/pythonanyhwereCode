import csv
import os


def script_laureandi_csv(path):
    file = ''
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file = filename
            break
        elif filename.endswith(".xlsx"):
            raise FileNotFoundError
    with open(path + file, 'r') as data:
        csv_data = csv.reader(data, delimiter='\t', skipinitialspace=True)

        # si trova la prima riga e colonna in cui cominciano i nomi dei relatori triennale

        for file in csv_data:
            for col in range(0, len(file)):

                if file[col] == "Relatore":
                    rightColRelatore = col
                    break
            else:
                continue
            break

        print(file)
        print(rightColRelatore)

        # variabile per memorizzare il numero di laureandi triennali
        lau_triennali = 0
        # variabile per memorizzare il numero di laureandi magistrali
        lau_magistrali = 0

        relatori_tri = {}
        relatori_mag = {}

        caratteri_speciali = ["'", "À", "È", "É", "Ì", "Ò", "Ù", "`"]
        caratteri_normali = ["", "A", "E", "E", "I", "O", "U", ""]

        # conteggio dei laureandi triennali e rispettivi relatori
        for file in csv_data:
            # si usa file[0] per indicare il primo campo che corrisponde alla prima colonna

            if file[rightColRelatore] == 'MAGISTRALE' or file[rightColRelatore] == '':
                break
            else:
                lau_triennali += 1
                prof = file[rightColRelatore].split()
                if len(prof) > 2:
                    file[rightColRelatore] = prof[0] + ' ' + prof[1]
                else:
                    file[rightColRelatore] = prof[0]
                    for i, j in zip(caratteri_speciali, caratteri_normali):
                        file[rightColRelatore] = file[rightColRelatore].replace(i, j)
                # nel file csv il campo corrispondente a file[4] è quello che contiene il nome del relatore
                # lista contiene il numero di studenti che hanno come relatore il prof indicato da file[4]
                if file[rightColRelatore] in relatori_tri:
                    lista = relatori_tri[file[rightColRelatore]]
                    lista = lista + 1
                    relatori_tri[file[rightColRelatore]] = lista
                else:
                    relatori_tri[file[rightColRelatore]] = 1

        print('\n')
        # si trova la prima riga in cui cominciano i nomi dei relatori magistrali
        for file in csv_data:
            for col in range(0, len(file)):
                if file[col] == "Relatore":
                    rightColRelatore = col
                    break
            else:
                continue
            break
        print(file)
        print(rightColRelatore)
        # conteggio laureandi magistrali e rispettivi relatori
        for file in csv_data:
            lau_magistrali += 1
            prof = file[rightColRelatore].split()

            if len(prof) > 2:
                file[rightColRelatore] = prof[0] + ' ' + prof[1]
            else:
                file[rightColRelatore] = prof[0]
                for i, j in zip(caratteri_speciali, caratteri_normali):
                    file[rightColRelatore] = file[rightColRelatore].replace(i, j)
            # nel file csv il campo corrispondente a file[4] è quello che contiene il nome del relatore
            # lista contiene il numero di studenti che hanno come relatore il prof indicato da file[4]
            if file[rightColRelatore] in relatori_mag:
                lista = relatori_mag[file[rightColRelatore]]
                lista = lista + 1
                relatori_mag[file[rightColRelatore]] = lista
            else:
                relatori_mag[file[rightColRelatore]] = 1

        if lau_triennali % 10 <= lau_triennali // 10:
            commissioni_t = lau_triennali // 10
        else:
            commissioni_t = lau_triennali // 10 + 1

        if lau_magistrali % 10 <= lau_magistrali // 10:
            commissioni_m = lau_magistrali // 10
        else:
            commissioni_m = lau_magistrali // 10 + 1

        # dizionario che contiene la mappa prof->(numero laureandi, nome laureandi)
        # il numero di laureandi triennali, il numero di laureandi magistrali, numero commissioni triennali
        # numero commissioni magistrali
        commissioni_t = int(commissioni_t)
        commissioni_m = int(commissioni_m)

        return {'relatori_tri': relatori_tri, 'lau_triennale': lau_triennali, 'commissioni_t': commissioni_t,
                'relatori_mag': relatori_mag, 'lau_magistrale': lau_magistrali, 'commissioni_m': commissioni_m}
