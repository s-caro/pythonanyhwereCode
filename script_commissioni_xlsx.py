import os
from typing import Dict, List, Any

import xlrd


def script_commissioni_xlsx(path, n_slot):
    file = ''
    for filename in os.listdir(path):
        print(filename)
        if filename.endswith(".xlsx"):
            file = filename
            break
    workbook = xlrd.open_workbook(path + file)
    worksheet = workbook.sheet_by_index(0)

    # dizionario che associa ad ogni professore (key) una lista in cui ogni posizione indica
    # una slot temporale e l'oggetto la tipologia di disponibilità
    prof_to_disp = {}

    # si trova la riga dove comincia l'elenco dei professori
    inizio = 0
    for row in range(0, worksheet.nrows):
        for col in range(0, worksheet.ncols):
            if worksheet.cell_value(row, col) == "mattina" or worksheet.cell_value(row, col) == "pomeriggio":
                inizio = row + 1
                rightCol = col - 1
                print(rightCol)
                break
        else:
            continue
        break

    caratteri_speciali = ["'", "À", "È", "É", "Ì", "Ò", "Ù", "`"]
    caratteri_normali = ["", "A", "E", "E", "I", "O", "U", ""]

    for row in range(inizio, worksheet.nrows):
        # no conta quante volte il professore ha no come disponibilità
        no = 0
        var = worksheet.cell_value(row, rightCol)
        if var == '' or var == 'totale' or not(isinstance(var, str)):
            break

        else:
            for i, j in zip(caratteri_speciali, caratteri_normali):
                var = var.replace(i, j)
            prof_to_disp[var] = []
            for i in range(rightCol+1, n_slot+1):
                if worksheet.cell_value(row, i) == 'NO':
                    no = no + 1
                prof_to_disp[var].append(worksheet.cell_value(row, i))
            # se un professore non è mai disponibile non viene inserito
            print(var, prof_to_disp[var])
            if no == n_slot:
                del prof_to_disp[var]

    return prof_to_disp
