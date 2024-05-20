#!/usr/bin/env python3
# coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2023 Simon J. Greenhill'
__license__ = 'New-style BSD'

from nexus import NexusReader

template = '        <sequence id="seq_%(taxon)s" spec="Sequence" taxon="%(taxon)s" totalcount="2" value="0%(sequence)s"/>'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename", help='filename')
    args = parser.parse_args()
    
    nex = NexusReader(args.filename)
    
    for taxon in nex.data.matrix:
        sequence = "".join(nex.data.matrix[taxon])
        print(template % {'taxon': taxon, 'sequence': sequence})
