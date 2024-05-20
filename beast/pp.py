#!/usr/bin/env python3
# coding=utf-8
from collections import defaultdict

import sys
sys.path.append('../bin')
from common import getcsv

import newick
from treemaker import TreeMaker


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    args = parser.parse_args()
    
    clades = defaultdict(lambda: TreeMaker(nodelabels=True))
    
    seen = []
    for r in getcsv(args.filename):
        # postpend glottocode
        clf = "%s/%s" % (r['Classification'], r['Glottocode'])
        if r['Language'] not in seen:
            clades[r['Clade']].add(r['Language'], clf.replace("/", ", "))
        seen.append(r['Language'])
        
        
    print("# Clades")
    print("")
    for clade in sorted(clades):
        print("## Clade: %s" % clade)
        print("")
        a = newick.loads(clades[clade].write())[0]
        print(a.ascii_art())
        print("")
        print("")
        