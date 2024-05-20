#!/usr/bin/env python3
# coding=utf-8
"""Tallies with datasets have cognates"""

import codecs
from pathlib import Path
from collections import Counter

from extract import getcsv, getrecords

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Tallies Cognates In Datasets')
    parser.add_argument("cldfmetadata", help='cldfmetadata', type=Path)
    parser.add_argument(
        "--cognates", dest='cognates',
        help="add published cognate sets", action='store', default=None, type=Path
    )
    parser.add_argument(
        "--remap", dest='remap',
        help="remap concepts", action='store', default=None, type=Path
    )
    args = parser.parse_args()

    if not args.cldfmetadata.exists():
        raise IOError("CLDF metadata file %s does not exist" % args.cldfmetadata)

    # load cognates
    cognates = {}
    if args.cognates:
        if not args.cognates.exists():
            raise IOError("Remapping file %s does not exist" % args.cognates)
        cognates = {r['lexicon_id']: r for r in getcsv(args.cognates)}

    # load remappings
    remap = {}
    if args.remap:
        if not args.remap.exists():
            raise IOError("Remapping file %s does not exist" % args.remap)
        remap = {
            r['ID']: get_concepticon_label(r['Concepticon_ID'], r['Concepticon_Gloss'])
            for r in getcsv(args.remap)
        }
    
    tally = Counter()
    for r in getrecords(args.cldfmetadata, remap, cognates):
        if r['Source'] and r['Cognacy']:
            tally[r['Source']] += 1
    
    for dataset in sorted(tally):
        print("%-30s\t%d" % (dataset, tally[dataset]))
        