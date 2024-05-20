#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'

from collections import Counter
from lingpy.basic.wordlist import Wordlist
import sys
import csvw
from pathlib import Path

BASE = Path(__file__).parent

sys.path.append('../bin')
from common import getcsv

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("details", help='filename')
    parser.add_argument("filename", help='filename')
    args = parser.parse_args()
    
    clades = {r['Taxon']: r['Clade'] for r in getcsv(args.details)}
    
    wl = Wordlist(str(args.filename))
    counter = Counter()
    for w in wl:
        lang, concept, *_ = wl[w]
        if not clades.get(lang):
            print(wl[w])
        counter[clades.get(lang)] += 1
    
    for k, v in counter.most_common():
        print("%20s\t%d" % (k, v))