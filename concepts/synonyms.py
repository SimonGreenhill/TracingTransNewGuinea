#!/usr/bin/env python3
# coding=utf-8
import sys
from collections import Counter
from pathlib import Path

from lingpy.basic.wordlist import Wordlist

sys.path.append('../bin')
from common import getcsv

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename', type=Path)
    parser.add_argument(
        '-f', "--filter", dest='filter',
        help="filter lexemes to only be those belonging to the concepts in this csv file",
        action='store', type=Path, default=None
    )
    args = parser.parse_args()

    assert args.filename.exists(), 'Filename %s does not exist!' % args.filename
    
    concepts = None
    if args.filter:
        assert args.filter.exists(), 'Filter filename %s does not exist!' % args.filter
        concepts = {c['Concept'] for c in getcsv(args.filter)}
    
    wl = Wordlist(str(args.filename))
    
    lexemes = Counter()
    for w in wl:
        # ['kobon', '1503_SALIVA', 'kɨñu', 'kɨñu', ['k', 'ɨ', 'ɲ', 'u'], '+', 'pawley-2013', 0]
        lang, concept, *_ = wl[w]
        
        if concepts and concept not in concepts:
            continue
        
        lexemes[(lang, concept)] += 1
    
    synonyms = [s for s in lexemes if lexemes[s] > 1]
    
    total_syn = 0
    for i, s in enumerate(sorted(synonyms), 1):
        print(i, s, lexemes[s])
        total_syn += lexemes[s]
    print("\n")
    
    lexemes = sum(lexemes.values())
    
    print("\nTOTAL SYNONYMS: %5d/%6d (%0.2f%%)" % (total_syn, lexemes, (total_syn/lexemes)*100))
        