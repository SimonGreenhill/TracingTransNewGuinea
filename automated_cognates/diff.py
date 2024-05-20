#!/usr/bin/env python3
# coding=utf-8
"""Calculates the Difference in languages between two datasets"""

from lingpy.basic.wordlist import Wordlist

def get_languages(filename):
    wl = Wordlist(filename)

    languages = set()
    for w in wl:
        lang, *_ = wl[w]
        languages.add(lang)
    return languages

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("filename1", help='filename')
    parser.add_argument("filename2", help='filename')
    parser.add_argument(
        '-v', "--verbose", dest='verbose',
        help="increases verbosity", action='store_true'
    )
    args = parser.parse_args()


    lang1 = get_languages(args.filename1)
    lang2 = get_languages(args.filename2)
    
    for l in sorted(lang1 | lang2):
        
        if l in lang1 and l in lang2:
            continue
        elif l in lang1 and l not in lang2:
            print("<", l)
        elif l not in lang1 and l in lang2:
            print(">", l)
        else:
            raise ValueError('wtf')

    