#!/usr/bin/env python3
# coding=utf-8
"""Checks that the concepts are those listed in the concept list"""
import sys
from collections import Counter
from pathlib import Path

from lingpy.basic.wordlist import Wordlist

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    args = parser.parse_args()
    
    wl = Wordlist(str(args.filename))
    tally = {
        'doculect': Counter(),
        'concept': Counter(),
        'autocogid': Counter(),
    }
    for i, w in enumerate(wl, 1):
        w = dict(zip(wl.columns, wl[w]))
        for k in tally:
            tally[k][w[k]] += 1

    for k in tally:
        print(k, len(tally[k]))
        #print(tally[k])
        #print()
    print("lexemes", i)