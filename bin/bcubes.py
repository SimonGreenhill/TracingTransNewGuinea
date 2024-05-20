#!/usr/bin/env python3
# coding=utf-8

from pathlib import Path
from lingpy import Wordlist
from lingpy import Wordlist
from lingpy.evaluate.acd import bcubes, diff

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Calculates B-Cubed Score')
    parser.add_argument("input", help='filename', type=Path)
    parser.add_argument("output", help='filename', type=Path)
    args = parser.parse_args()

    wl = Wordlist(str(args.input))
    bcubes(wl, 'cogid', 'autocogid')
    diff(wl, 'cogid', 'autocogid', pprint=False, filename=str(args.output.with_suffix("")))
