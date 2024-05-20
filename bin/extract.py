#!/usr/bin/env python3
# coding=utf-8
"""Extracts data from CLDF"""

import codecs
from collections import deque
from pathlib import Path

import csvw
from pycldf import Dataset


def getcsv(filename, delimiter=","):
    """Reads a CSV file"""
    with csvw.UnicodeDictReader(filename, delimiter=delimiter) as reader:
        for row in reader:
            yield(row)


def get_concepticon_label(concepticon_id, concepticon_gloss):
    concepticon_gloss = concepticon_gloss.replace(" ", "_").replace("(", "").replace(")", "")
    return "%s_%s" % (concepticon_id, concepticon_gloss)


def getrecords(cldfmetadata, remap=None, cognates=None):
    """
    Returns a generator of records from the given CLDF dataset in `cldfmetadata`.
    
    - cldfmetadata - a CLDF metadata.json file
    - remap - a remapping dictionary of {parameter_id} => {new_parameter_id}
    - cognates - a dictionary of {lexicon_id} => {cognate_set_id}
    
    """
    tng = Dataset.from_metadata(cldfmetadata)
    
    remap = remap if remap else {}
    cognates = cognates if cognates else {}
    
    # check cognates are all integery
    try:
        cognates = {c: int(cognates[c]) if cognates[c] is not None else None for c in cognates}
    except (TypeError, ValueError):
        raise ValueError("Cognate sets should all be integers")

    concepts = {
        r.id: get_concepticon_label(r.data['Concepticon_ID'], r.data['Concepticon_Gloss'])
        for r in tng.objects('ParameterTable')
        if r.data['Concepticon_ID'] and r.data['Concepticon_Gloss']
    }

    for row in tng.objects('FormTable'):
        out = row.data.copy()
        
        # squash source to one entry as they're always a 1:1 mapping, and this helps filtering later
        if out['Source']:
            out['Source'] = out['Source'][0]
        if len(out['Source']) == 0:
            out['Source'] = ''
        
        # set concept
        # if there's a remapping in place, then set concept to "{Concepticon_ID}_{Concepticon_Gloss}"
        if out['Parameter_ID'] in remap:
            out['Concept'] = remap.get(out['Parameter_ID'])
        # if there's a concepticon mapping for this parameter use that
        elif concepts.get(out['Parameter_ID']):
            out['Concept'] = concepts.get(out['Parameter_ID'])
        # otherwise use default mapping
        else:
            out['Concept'] = out['Parameter_ID']
        
        # patch in cognate data
        out['Cognacy'] = cognates.get(out['Local_ID'], None)
            
        # remove unneeded
        for k in ['Graphemes', 'Profile', 'Parameter_ID']:
            del(out[k])
        
        yield out

# simple but functionalised to enable testing of core capabilities
def remove(records, function):
    """Removes items from the iterator `records` if they fail to match `function`"""
    yield from [r for r in records if function(r) == False]


def none_to_str(x):
    """Replace `None` with empty string and make sure everything is a string"""
    return str(x) if x is not None else ""


def convert_to_source_labels(records, source_labels):
    for r in records:
        r['Language_ID'] = "%s_%s" % (r['Language_ID'], source_labels.get(r['Source'], ''))
        yield r


def to_wordlist(records, filename):
    """Write `records` to `filename` in lingpy Wordlist format"""
    with codecs.open(filename, 'w', 'utf8') as handle:
        handle.write("# Wordlist\n\n")
        handle.write("# DATA\n")
        handle.write("ID	DOCULECT	CONCEPT	VALUE	FORM	TOKENS	NOTE	SOURCE	COGID\n")
        
        for i, r in enumerate(records, 1):
            
            out = [
                r['Local_ID'],
                r['Language_ID'],
                r['Concept'],
                r['Value'],
                r['Form'],
                " ".join(r['Segments']),
                none_to_str(r['Comment']),
                none_to_str(r['Source']),
                none_to_str(r['Cognacy'])
            ]
            #print("WRITE", out)
            handle.write("\t".join(out) + "\n")
    return i


def add_singleton_cognates(records):
    records = list(records)  # consume generators as we need to preparse the records
    known = {int(r['Cognacy']) for r in records if r['Cognacy']}
    # +2 here means we include the last number AND add one extra one in case we have all the 
    # numbers covered from min-max
    unused = set(range(1, len(records) + 2)) ^ set(known)
    # convert to deque so pop is consistent order 1-n, pop from set is random order (but fast)
    unused = deque(unused)
    unused.reverse()
    for r in records:
        if not r['Cognacy']:
            r['Cognacy'] = unused.pop()
        yield r


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extracts datasets')
    parser.add_argument("cldfmetadata", help='cldfmetadata', type=Path)
    parser.add_argument("output", help='output', type=Path)
    parser.add_argument(
        "--source", dest='source',
        help="extract source only", action='store', default=None
    )
    parser.add_argument(
        "--concepts", dest='concepts',
        help="extract concepts only", action='store', default=None, type=Path
    )
    parser.add_argument(
        "--ignore", dest='ignore',
        help="ignore these languages", action='store', default=None, type=Path
    )
    parser.add_argument(
        "--cognates", dest='cognates',
        help="add published cognate sets", action='store', default=None, type=Path
    )
    parser.add_argument(
        "--remap", dest='remap',
        help="remap concepts", action='store', default=None, type=Path
    )
    parser.add_argument(
        "--labelsource", dest='labelsource',
        help="label languages with source", action='store', default=None, type=Path
    )
    args = parser.parse_args()

    if not args.cldfmetadata.exists():
        raise IOError("CLDF metadata file %s does not exist" % args.cldfmetadata)


    # load languages to ignore
    ignore = {}
    if args.ignore:
        if not args.ignore.exists():
            raise IOError("Ignore Language file %s does not exist" % args.ignore)
        ignore = {r['ID']: r for r in getcsv(args.ignore)}

    # load sources
    sources = {}
    if args.labelsource:
        if not args.labelsource.exists():
            raise IOError("Source Label file %s does not exist" % args.labelsource)
        sources = {r['ID']: r['Label'] for r in getcsv(args.labelsource)}
        
    # load cognates
    cognates = {}
    if args.cognates:
        if not args.cognates.exists():
            raise IOError("Remapping file %s does not exist" % args.cognates)
        cognates = {r['lexicon_id']: r['cognateset_id'] for r in getcsv(args.cognates)}

    # load remappings
    remap = {}
    if args.remap:
        if not args.remap.exists():
            raise IOError("Remapping file %s does not exist" % args.remap)
        remap = {
            r['ID']: get_concepticon_label(r['Concepticon_ID'], r['Concepticon_Gloss'])
            for r in getcsv(args.remap)
        }
    
    # load wanted concepts if required
    wanted_concepts = None
    if args.concepts:
        if not args.concepts.exists():
            raise IOError("Concept filter file %s does not exist" % args.concepts)
        wanted_concepts = set(r['Concept'] for r in getcsv(args.concepts))
    
    records = [r for r in getrecords(args.cldfmetadata, remap, cognates)]
    n = len(records)
    # remove unwanted languages
    records = list(remove(records, lambda r: r['Language_ID'] in ignore))
    
    print("%d / %d remaining after ignoring %d unwanted languages" % (len(records), n, len(ignore)))
    
    # filter by source
    if args.source:
        records = list(remove(records, lambda r: r['Source'] != args.source))
    
    # remove unwanted concepts if required
    if wanted_concepts:
        n = len(records)
        records = list(remove(records, lambda r: r['Concept'] not in wanted_concepts))
        print("%d / %d remaining after ignoring unwanted concepts" % (len(records), n))
    
    # relabel sources
    if sources:
        records = convert_to_source_labels(records, sources)
    
    records = add_singleton_cognates(records)

    n = to_wordlist(records, args.output)
    print("%d records written to %s" % (n, args.output))