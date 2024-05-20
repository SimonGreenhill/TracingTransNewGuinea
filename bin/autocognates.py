#!/usr/bin/env python3
# coding=utf-8
import logging
from pathlib import Path
from lingpy import LexStat

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Does something.')
    parser.add_argument("input", help='filename', type=Path)
    parser.add_argument("output", help='filename', type=Path)
    parser.add_argument(
        "--method", dest='method',
        help="use method", action='store', default='lexstat',
        choices=('lexstat', 'infomap', 'turchin', 'edit-dist', 'sca')
    )
    args = parser.parse_args()
    
    lex = LexStat(str(args.input))
    
    # turn off excessive logging.INFO and logging.DEBUG output
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(logging.ERROR)
    
    if args.method == 'lexstat':
        lex.get_scorer(runs=1000)
        lex.cluster(method='lexstat', ref="autocogid", threshold=0.60)
    elif args.method == 'infomap':
        lex.get_scorer(runs=1000)
        lex.cluster(method="lexstat", ref="autocogid", threshold=0.55, cluster_method='infomap')
    elif args.method in ('turchin', 'edit-dist', 'sca'):
        lex.cluster(method=args.method, ref="autocogid")
    
    lex.output("tsv", filename=str(args.output.with_suffix("")))


