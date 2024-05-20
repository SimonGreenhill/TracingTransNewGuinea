#!/usr/bin/env python3
# coding=utf-8
"""..."""
from collections import defaultdict
import xml.etree.ElementTree as ET
from collections import Counter

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    parser.add_argument(
        '-v', "--verbose", dest='verbose',
        help="increases verbosity", action='store_true'
    )
    args = parser.parse_args()

    tree = ET.parse(args.filename)
    taxa, cognates = set(), defaultdict(set)
    for seq in tree.getroot().findall('./data/sequence'):
        taxon = seq.attrib['taxon']
        taxa.add(taxon)
        for i, s in enumerate(seq.attrib['value']):
            if s == '1':
                cognates[i].add(taxon)
    
    nonzero, nonsingle = 0, 0
    
    tally = Counter()
    for i in range(0, max(cognates)):
        if len(cognates[i]):
            nonzero += 1
        if len(cognates[i]) > 1:
            nonsingle += 1
        tally[len(cognates[i])] += 1
        
    print("taxa", len(taxa))
    print("cognates + 1", nonzero)
    print("cognates + 2", nonsingle)


    for i in range(0, max(tally)):
        print("%5d\t%d" % (i, tally.get(i, 0)))
