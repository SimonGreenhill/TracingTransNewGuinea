#!/usr/bin/env python3
# coding=utf-8
"""Checks that the concepts are those listed in the concept list"""
import sys
from collections import Counter
from pathlib import Path

from lingpy.basic.wordlist import Wordlist

sys.path.append('../bin')
from common import getcsv


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("concepts", help='filename')
    parser.add_argument("filename", help='filename')
    parser.add_argument(
        '-v', "--verbose", dest='verbose',
        help="increases verbosity", action='store_true'
    )
    args = parser.parse_args()
    
    wl = Wordlist(str(args.filename))
    concepts = Counter({r['Concept']: 0 for r in getcsv(args.concepts)})
    languages = Counter()
    errors = 0
    for w in wl:
        # ['kobon', '1503_SALIVA', 'kɨñu', 'kɨñu', ['k', 'ɨ', 'ɲ', 'u'], '+', 'pawley-2013', 0]
        lang, concept, *_ = wl[w]
        if concept not in concepts:
            print("UNWANTED", lang, concept)
            errors += 1
        else:
            concepts[concept] += 1
        languages[lang] += 1
    
    for c in concepts:
        if concepts[c] == 0:
            print("MISSING", c)
            errors += 1
    
    for l in languages:
        if languages[l] < 100:
            print("ERROR Language", l, languages[l])
            errors += 1
        if l.startswith('proto'):
            print("ERROR Bad Language", l)
        if l.startswith('unknown'):
            print("ERROR Bad Language", l)
        
    if errors:
        raise ValueError("Errors found: %d" % errors)