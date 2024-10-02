import os

import xlrd


def script_laureandi_xlsx(path):
    file = ''
    for filename in os.listdir(path):
        if filename.endswith(".xlsx"):
            file = filename
            break
    workbook = xlrd.open_workbook(path + file)
    worksheet = workbook.sheet_by_index(0)

    # variabile per memorizzare il numero di laureandi triennali
    lau_triennali = 0
    # variabile per memorizzare il numero di laureandi magistrali
    lau_magistrali = 0

    relatori_tri = {}
    relatori_mag = {}
    # riga alla quale finiscono i laureandi triennali
    first_end = 0

    caratteri_speciali = ["'", "À", "È", "É", "Ì", "Ò", "Ù", "`"]
    caratteri_normali = ["", "A", "E", "E", "I", "O", "U", ""]

    first_name = 0
    for row in range(0, worksheet.nrows):
        for col in range(0, worksheet.ncols):
            if worksheet.cell_value(row, col) == "Relatore":
                first_name = row + 1
                rightCol = col

                break
        else:
            continue
        break
    # conteggio dei laureandi triennali e rispettivi relatori
    for row in range(first_name, worksheet.nrows):
        # var contiene il nome del professore relatore
        var = worksheet.cell_value(row, rightCol)
        if worksheet.cell_value(row, rightCol) == '':
            first_end = row
            break
        else:
            lau_triennali += 1
            prof = var.split()
            if len(prof) > 2:
                var = prof[0] + ' ' + prof[1]
            else:
                var = prof[0]
                for i, j in zip(caratteri_speciali, caratteri_normali):
                    var = var.replace(i, j)
            # si usa worksheet.cell_value(row, 4) per indicare il nome del relatore
            # lista contiene il numero di studenti che hanno come relatore il prof
            # indicato da worksheet.cell_value(row, 4)
            if var in relatori_tri:
                lista = relatori_tri[var]
                lista = lista + 1
                relatori_tri[var] = lista
            else:
                relatori_tri[var] = 1
    # conteggio laureandi magistrali e rispettivi relatori
    for row in range(first_end, worksheet.nrows):
        var = worksheet.cell_value(row, rightCol)
        if var == 'Relatore' or worksheet.cell_value(row, rightCol) == 'MAGISTRALE' \
                or worksheet.cell_value(row, rightCol) == '':
            continue
        else:
            lau_magistrali += 1
            prof = var.split()
            if len(prof) > 2:
                var = prof[0] + ' ' + prof[1]
            else:
                var = prof[0]
                for i, j in zip(caratteri_speciali, caratteri_normali):
                    var = var.replace(i, j)
            # si usa worksheet.cell_value(row, 4) per indicare il nome del relatore
            # lista contiene il numero di studenti che hanno come relatore il prof
            # indicato da worksheet.cell_value(row, 4)
            if var in relatori_mag:
                lista = relatori_mag[var]
                lista = lista + 1
                relatori_mag[var] = lista
            else:
                relatori_mag[var] = 1

    if lau_triennali % 10 <= lau_triennali // 10:
        commissioni_t = lau_triennali // 10
    else:
        commissioni_t = lau_triennali / 10 + 1

    if lau_magistrali % 10 <= lau_magistrali // 10:
        commissioni_m = lau_magistrali // 10
    else:
        commissioni_m = lau_magistrali // 10 + 1

    commissioni_t = int(commissioni_t)
    commissioni_m = int(commissioni_m)

    # dizionario che contiene la mappa prof->numero laureandi triennali, prof->numero laureandi magistrale
    # il numero di laureandi triennali, il numero di laureandi magistrali, numero commissioni triennali
    # numero commissioni magistrali
    print(relatori_tri)
    print(relatori_mag)
    return {'relatori_tri': relatori_tri, 'lau_triennale': lau_triennali, 'commissioni_t': commissioni_t,
            'relatori_mag': relatori_mag, 'lau_magistrale': lau_magistrali, 'commissioni_m': commissioni_m}
