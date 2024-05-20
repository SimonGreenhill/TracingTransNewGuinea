#!/usr/bin/env python3
# coding=utf-8

from collections import defaultdict, Counter
from lingpy.basic.wordlist import Wordlist

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    args = parser.parse_args()
    
    wl = Wordlist(args.filename)
    
    languages, concepts = defaultdict(set), set()
    for w in wl:
        row = dict(zip(wl.columns, wl[w]))
        if not int(row['autocogid']):
            raise ValueError("BAD: %r" % row)
        else:
            languages[row['doculect']].add(row['concept'])
            concepts.add(row['concept'])
    
    totals = Counter()
    for lang in languages:
        totals[lang] = len([c for c in concepts if c in languages[lang]])
    
    for k, v in totals.most_common():
        print("\t".join([
            "%-40s" % k,
            '%4d' % totals[k],
            '%4d' % len(concepts),
            '%0.2f' % ((totals[k] / len(concepts))*100)
        ]))
