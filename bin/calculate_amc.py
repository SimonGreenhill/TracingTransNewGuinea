#!/usr/bin/env python3
# coding=utf-8
from pathlib import Path
from lingpy.basic.wordlist import Wordlist
from lingpy.compare.sanity import average_coverage

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Calculates Average Mutual Coverage.')
    parser.add_argument("filename", help='filename', type=Path)
    args = parser.parse_args()

    assert args.filename.exists(), 'Filename %s does not exist!' % args.filename
    assert not args.filename.is_dir(), 'Filename %s cannot be a directory!' % args.filename
    
    wl = Wordlist(str(args.filename))
    print("Wordlist,Languages,Concepts,Entries,AverageMutualCoverage")
    print("%s,%d,%d,%d,%f" % (
        args.filename.stem,
        wl.width,
        wl.height,
        len(wl),
        average_coverage(wl)
    ))
