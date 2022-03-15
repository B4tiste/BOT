from io import *
from itertools import combinations
from collections import defaultdict
from random import choice
from time import time

words = defaultdict(list)


def search_for1(letters):
    ret = []
    for sz in range(len(letters), 0, -1):
        for _letters in combinations(letters, sz):
            key = ''.join(sorted(_letters))
            if key in words:
                ret += words[key]
        if ret != []:
            return sz, list(set(ret))
    return 0, []


def search_for2(letters):
    letters = sorted(letters)
    d = defaultdict(list)
    for key in words.keys():
        i, j = 0, 0
        while j < len(key) and i < len(letters):
            if key[j] != letters[i]:
                i += 1
            else:
                i += 1
                j += 1
        if j == len(key):
            d[len(key)].extend(words[key])
    best_len = max(d.keys())
    return best_len, d[best_len]


def search_for(letters):
    if 2 ** len(letters) > len(words):
        # print('  use v2; O('+str(len(words))+')')
        return search_for2(letters)
    else:
        # print('  use v1; O('+str(2 ** len(letters))+')')
        return search_for1(letters)


# chargement du dictionnaire
infile = open('Ressources/wordlist.txt', 'r')
wc = 0
while True:
    line = infile.readline()
    if line == str():
        break
    wc += 1
    line = line.strip('\n')
    key = ''.join(sorted(line)).replace('-', '')
    words[key].append(line)
infile.close()
#print(str(wc) + ' mots présents dans le dictionnaire'+'\n')


# boucle principale
# while True:

def analyse(liste_lettre):
    # t = input('Entrez un tirage : ').strip('\n')
    # tstart = time()
    sz, lst = search_for(liste_lettre)

    return str(lst)
