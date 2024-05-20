#!/usr/bin/env python3
# coding=utf-8
"""See what would be combined"""
import sys
from collections import Counter, defaultdict

from lingpy.basic.wordlist import Wordlist

sys.path.append('../bin')
from common import getcsv


EXAMPLE_ROW = {
    "doculect": "kuman_t69",
    "concept": "2102_BURN",
    "value": "gakʝkwa",
    "form": "gakʝkwa",
    "tokens": ["g", "a", "k", "ʝ", "k", "w", "a"],
    "note": "",
    "source": "trefry-1969",
    "cogid": 1,
}


def reformat(data):
    records = []
    for d in data:
        records.extend(data[d])
    return sorted(records, key=lambda d: (d['concept'], d['doculect']))

def pp(row):
    return " %-20s\t%-20s\t%20s\t%10s" % (row['concept'], row['doculect'][0:20], row['form'], row['cogid'])


def reformat(data):
    records = Counter()
    for d in data:
        for r in data[d]:
            records[(r['concept'], r['form'])] += 1 
    
    return sorted([
        (r[0][0], r[1], r[0][1]) for r in records.most_common()
    ])
    
def pp(concept, count, form):
    return " %-30s\t%-20s\t%2d" % (concept, form, count)


if __name__ == '__main__':
    wl = Wordlist('transnewguinea_tng.remapped.tsv')
    languages = defaultdict(lambda: defaultdict(list))
    for w in wl:
        row = dict(zip(wl.columns, wl[w]))
        lang = row['doculect'].rsplit('_', 1)[0]
        languages[lang][row['doculect']].append(row)
        
    for lang in sorted(languages):
        if len(languages[lang]) == 1:
            continue
            
        print("%30s << %s" % (lang, ", ".join(languages[lang])))
        for row in reformat(languages[lang]):
            print(pp(*row))
        
        print('----------------------------------------------------------------')
        print()
    