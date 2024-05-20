#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'

import sys
from nexus import NexusReader

import csvw

sys.path.append('../bin')
from common import getcsv

def to_label(clade, lang):
    clade = clade.replace(" ", "").replace(".", "_")
    return "%s_%s" % (clade, lang)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("data", help='filename')
    parser.add_argument("trees", help='filename')
    parser.add_argument(
        '-v', "--verbose", dest='verbose',
        help="increases verbosity", action='store_true'
    )
    args = parser.parse_args()

    nex = NexusReader(args.trees)
    remap = {r['Language']: to_label(r['Clade'], r['Language']) for r in getcsv(args.data)}
    
    # for r in remap:
    #     print("%20s\t->\t%20s" % (r, remap[r]))
    
    del(nex.blocks['taxa'])
    nex.trees.translators = {i: '"%s"' % remap[taxon] for (i, taxon) in nex.trees.translators.items()}

    print(nex.write())

        