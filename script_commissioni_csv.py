import csv
import os


def script_commissioni_csv(path, n_slot):
    file = ''
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            file = filename
            break
        elif filename.endswith(".xlsx"):
            raise FileNotFoundError
    with open(path + file, 'r') as data:
        csv_data = csv.reader(data, delimiter='\t')

        # si devono saltare le prime 8 righe per arrivare all'elenco dei professori e giorni disponibili
        for date in csv_data:
            for col in range(0, len(date)):
                if date[col] == "mattina" or date[col] == "pomeriggio":
                    rightCol = col - 1
                    print(rightCol)
                    print(date)
                    break
            else:
                continue
            break
        # dizionario che associa ad ogni professore (key) una lista in cui ogni posizione indica
        # una slot temporale e l'oggetto la tipologia di disponibilità
        prof_to_disp = {}
        caratteri_speciali = ["'", "À", "È", "É", "Ì", "Ò", "Ù", "`"]
        caratteri_normali = ["", "A", "E", "E", "I", "O", "U", ""]
        for files in csv_data:
            # no conta quante volte il professore ha no come disponibilità
            no = 0
            if files[rightCol] == '' or files[rightCol] == 'totale' or not(isinstance(files[rightCol], str)):
                break

            else:
                for i, j in zip(caratteri_speciali, caratteri_normali):
                    files[rightCol] = files[rightCol].replace(i, j)
                prof_to_disp[files[rightCol]] = []
                var = prof_to_disp[files[rightCol]]
                for i in range(rightCol+1, n_slot+1):
                    if files[i] == 'NO':
                        no = no + 1
                    var.append(files[i])
                # se un professore non è mai disponibile non viene inserito
                if no == n_slot:
                    del prof_to_disp[files[rightCol]]

    return prof_to_disp
