#!/usr/bin/env python3
# coding=utf-8

from collections import defaultdict
from lingpy.basic.wordlist import Wordlist

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    parser.add_argument("output", help='filename')
    parser.add_argument(
        '-t', "--threshold", dest='threshold',
        help="remove languages below the threshold", action='store', default=1, type=int
    )
    args = parser.parse_args()
    
    wl = Wordlist(args.filename)
    
    languages = defaultdict(set)
    for w in wl:
        lang, concept, *_ = wl[w]
        languages[lang].add(concept)
    
    keep = []
    for i, l in enumerate(languages, 1):
        if len(languages[l]) > args.threshold:
            keep.append(l)
            print("KEEP: %d\t%40s\t%d" % (i, l, len(languages[l])))
        else:
            print("REMOVE: %d\t%40s\t%d" % (i, l, len(languages[l])))
    
    print("%d languages kept" % len(languages))
        
    wl.output("tsv",
        filename=args.output if not args.output.endswith('.tsv') else args.output.replace(".tsv", ""),
        subset=True,
        rows={"doculect": "in "+str(keep)}
    )