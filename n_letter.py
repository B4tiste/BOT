# -*- coding: utf-8 -*-
"""
Code du Jeu 'Des Chiffres et Des Lettres'

@author: batiste
"""


def analyse(liste_lettre):
    f_dico = open('Ressources/wordlist.txt', 'r')

    str_dico = f_dico.read()
    str_dico_ori = f_dico.read()

    f_dico.close()

    str_dico = str_dico.replace("\n", ',').replace("-", "").lower()
    str_dico_ori = str_dico_ori.replace("\n", ',').lower()

    lst_dico = str_dico.split(',')
    lst_dico_ori = str_dico.split(',')

    cpy_dico_sorted = ['']*len(lst_dico)

    # print(len(lst_dico))
    # print(len(cpy_dico_sorted))

    """for i in range(len(sorted(lst_dico[5]))):
        word = word + sorted(lst_dico[5])[i]

    print(word)"""

    # On tri les lettres composant chaque mots par ordre alphabétique

    word_sort = ''
    for i in range(len(lst_dico)):
        for y in range(len(lst_dico[i])):
            word_sort = word_sort + sorted(lst_dico[i])[y]

        cpy_dico_sorted[i] = word_sort

        word_sort = ''

    # print(lst_dico[0:10])
    # print(cpy_dico_sorted[0:10])

    # print(str_lettre)

    lst_lettre_sort = sorted(liste_lettre)

    str_lettre_sort = ''

    for i in range(len(lst_lettre_sort)):
        str_lettre_sort = str_lettre_sort + lst_lettre_sort[i]

    # print(str_lettre_sort)

    mots_correspondant = []

    if str_lettre_sort in cpy_dico_sorted:

        # print('a')

        for i in range(len(cpy_dico_sorted)):
            if cpy_dico_sorted[i] == str_lettre_sort:

                mots_correspondant.append(lst_dico_ori[i])

        return str(mots_correspondant)

    else:

        return False
