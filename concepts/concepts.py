#!/usr/bin/env python3
# coding=utf-8
import sys
from pathlib import Path
from collections import Counter

import csvw
from lingpy.basic.wordlist import Wordlist

sys.path.append('../bin')
from common import getcsv, get_concepticon_label

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename', type=Path)
    parser.add_argument("swadesh", help='filename', type=Path)
    parser.add_argument("output", help='filename', type=Path)
    args = parser.parse_args()

    assert args.filename.exists(), 'Filename %s does not exist!' % args.filename
    assert not args.filename.is_dir(), 'Filename %s cannot be a directory!' % args.filename
    
    assert args.swadesh.exists(), 'Swadesh %s does not exist!' % args.filename
    assert not args.swadesh.is_dir(), 'Swadesh %s cannot be a directory!' % args.filename
    
    swadesh = [
        get_concepticon_label(row['concepticon_id'], row['gloss'])
        for row in getcsv(args.swadesh)
    ]
    
    wl = Wordlist(str(args.filename))
    concepts = Counter()
    for w in wl:
        # ['kobon', '1503_SALIVA', 'kɨñu', 'kɨñu', ['k', 'ɨ', 'ɲ', 'u'], '+', 'pawley-2013', 0]
        concepts[wl[w][1]] += 1
    
    seen = set()
    with csvw.UnicodeWriter(args.output) as writer:
        writer.writerow(["Concept", "Count", "Swadesh"])
        for o in concepts.most_common():
            s = 'Swadesh200' if o[0] in swadesh else ''
            writer.writerow([o[0], o[1], s])
            seen.add(o[0])
    
    for s in sorted(swadesh):
        if s not in seen:
            print("UNSEEN: %s" % s)
