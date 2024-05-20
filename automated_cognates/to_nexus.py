#!/usr/bin/env python3
# coding=utf-8
from collections import defaultdict
from nexus import NexusWriter
from nexusmaker import NexusMaker, Record, CognateParser
from lingpy.basic.wordlist import Wordlist


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    parser.add_argument("nexus", help='filename')
    args = parser.parse_args()
    
    cp = CognateParser()
    
    wl = Wordlist(args.filename)
    records = []
    for w in wl:
        row = dict(zip(wl.columns, wl[w]))
        records.append(Record(
            ID=w,
            Language=row['doculect'],
            Parameter=row['concept'],
            Item=row['form'],
            Cognacy=str(row['autocogid']),
        ))
        #print(row['autocogid'], cp.parse_cognate(row['autocogid']), cp.is_unique_cognateset(row['autocogid'][0]))
        
    maker = NexusMaker(records)
    #maker = NexusMakerAscertained(data)  # adds Ascertainment bias character
    #maker = NexusMakerAscertainedWords(data)  # adds Ascertainment character per word
    maker.write(filename=args.nexus)
