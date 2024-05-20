#!/usr/bin/env python3
# coding=utf-8
"""Collects and Tabulates B-Cubed Scores"""
import re
from collections import defaultdict
from pathlib import Path

import csvw

is_statistic = re.compile(r"""^\*\s+(.+):\s+(.*) \*$""")

def read_bcube_log(pathobj):
    # *************************
    # * B-Cubed-Scores        *
    # * --------------------- *
    # * Precision:     0.9935 *
    # * Recall:        0.8011 *
    # * F-Scores:      0.8870 *
    # *************************'
    delimiters = [
        "*************************",
        "*************************'",  # note bug '
        "* --------------------- *",
        '* B-Cubed-Scores        *',
    ]
    out = {'Precision': None, 'Recall': None, 'F-Scores': None}
    for line in pathobj.read_text().split("\n"):
        if line in delimiters:
            continue
        elif len(line.strip()) == 0:
            continue
        elif m := is_statistic.match(line):
            key, value = m.groups()
            if key not in out:
                raise ValueError("Unknown key %s" % key)
            out[key] = float(value)
        else:
            print("Unknown line: %r" % line)
    return out


def get_method(fileobj):
    return fileobj.name.split(".")[0:2]


def format_numbers(numbers):
    m = max(numbers)
    return ['%0.3f' % n if n is not m else '%0.3f*' % n for n in numbers]
    


if __name__ == '__main__':
    # collect results
    results = defaultdict(dict)
    for log in Path(__file__).parent.glob("*.log"):
        dataset, method = get_method(log)
        try:
            b = read_bcube_log(log)
        except Exception as e:
            raise Exception("`%s` encountered when reading %s" % (e, log))
            
        assert method not in results[dataset], 'Duplicate method? %s:%s' % (dataset, method)
        results[dataset][method] = b
    
    # write results
    methods = ['edit-dist', 'sca', 'turchin', 'lexstat', 'infomap']
    for metric in ("Precision", "Recall", "F-Scores"):
        print("# %s:\n" % metric)
        if metric == 'Precision':
            print("(fraction of received values that are relevant)\n")
        elif metric == 'Recall':
            print("(fraction of relevant instances returned)\n")

        header = ['Dataset']
        header.extend([m.replace("-dist", "") for m in methods])
        
        with csvw.UnicodeWriter('results-%s.csv' % metric.lower()) as writer:
            
            # write to csv
            writer.writerow(header)
            
            # pretty format for printing
            header[0] = "%-30s" % header[0]
            # print to screen
            print("\t".join(header))
            
            for dataset in sorted(results):
                row = [results[dataset][m].get(metric, '-') for m in methods]
                row.insert(0, dataset)
                # write to csv
                writer.writerow(row)
                
                # pretty format for printing
                row = format_numbers(row[1:])
                row.insert(0, "%-30s" % dataset)
                print("\t".join(row))

            print("")
