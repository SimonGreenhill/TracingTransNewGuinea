#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'

import sys
from collections import defaultdict
from pathlib import Path

import csvw

BASE = Path(__file__).parent

sys.path.append('../bin')
from common import getcsv

if __name__ == '__main__':
    
    original = {o['ID']: o for o in getcsv(BASE / 'transnewguinea-org/cldf/parameters.csv')}
    
    keeping_in_200w = {o['Concept'] for o in getcsv(BASE / 'concepts.csv')}
    
    n = 1
    for remapped in getcsv(BASE / 'remap.csv'):
        old = remapped['ID']
        new = remapped['Concepticon_Gloss']
        
        if keeping_in_200w:
            print(old, new)
        
        # o = original.get(remapped['ID'])
        # if o['Concepticon_ID'] != remapped['Concepticon_ID']:
        #     print("%3d. %40s remapped from '%s.%s' to '%s.%s'" % (
        #         n, remapped['ID'],
        #         o['Concepticon_ID'], o['Concepticon_Gloss'],
        #         remapped['Concepticon_ID'], remapped['Concepticon_Gloss']
        #     ))
        #     n += 1
