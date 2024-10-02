from builtins import list
from string import ascii_uppercase


def slot_temporali(n_slot):
    tot = n_slot

    lettere = []

    for c in ascii_uppercase:
        if tot is not 0:
            lettere.append(c)
            tot = tot - 1

    return lettere
