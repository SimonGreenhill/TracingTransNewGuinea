#!/usr/bin/env python3
# coding=utf-8
import sys
from nexus import NexusReader

import csvw

sys.path.append('../bin')
from common import getcsv

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    parser.add_argument("nexus", help='filename')
    parser.add_argument("output", help='filename')
    parser.add_argument(
        '-v', "--verbose", dest='verbose',
        help="increases verbosity", action='store_true'
    )
    args = parser.parse_args()

    nex = NexusReader(args.nexus)
    
    out = []
    for row in getcsv(args.filename):
        if row['Taxon'] in nex.data.taxa:
            out.append(row)  # labels are taxa
        elif row['Language'] in nex.data.taxa:
            out.append(row)  # labels are languages
    
    with csvw.UnicodeWriter(args.output) as writer:
        header = out[0].keys()
        writer.writerow(header)
        for o in out:
            writer.writerow([o[h] for h in header])