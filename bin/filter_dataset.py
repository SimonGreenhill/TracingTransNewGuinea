#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'

from pathlib import Path

import csvw

def get(filename, delimiter=","):
    with csvw.UnicodeDictReader(filename, delimiter=delimiter) as reader:
        for row in reader:
            yield(row)

def write(filename, out, delimiter=","):
    with csvw.UnicodeWriter(filename, delimiter=delimiter) as writer:
        header = out[0].keys()
        writer.writerow(header)
        for o in out:
            writer.writerow([o[h] for h in header])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("infilename", help='filename', type=Path)
    parser.add_argument("outfilename", help='filename', type=Path)
    parser.add_argument(
        "--missing", dest='missing',
        help="remove languages with fewer concepts than this", action='store', default=0, type=int
    )
    args = parser.parse_args()
    
    records = list(get(args.infilename))
    for row in get(args.infilename):
        print(row)
        quit()

