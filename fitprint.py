#! /usr/local/bin/python3

import argparse
# stdin
import sys
import subprocess
from functools import partial

from math import ceil

def cpi_lpi(txt, width=72, aspect=2, encoding='utf-8', wiggle=0.001, unit='mm'):
    if unit == 'mm':
        mmtoin = 0.039370079
        inwidth = width * mmtoin
    lines = txt.splitlines()
    maxlen = len(max(lines, key=lambda k: len(k)))
    cpi = maxlen / inwidth / (1 - wiggle)
    lpi = cpi / aspect
    return cpi, lpi

def fitprint(txt, width=72, aspect=2, encoding='utf-8', wiggle=0.001, unit='mm'):
    """
    width: mm
    aspect: character height/width aspect ratio
    wiggle: wiggle room; how much of the line's width to ignore
    """
    # this is the first thing we do so i think it's ok
    cpi, lpi = cpi_lpi(**locals())
    process = subprocess.Popen(['lp', '-o', 'cpi=' + str(cpi),
        '-o', 'lpi=' + str(lpi)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return process.communicate(input=txt.encode(encoding))

def main():
    prog = 'fitprint'

    argparser = argparse.ArgumentParser(
        description='''A utility for printing with `lp` that reads from STDIN /
        files, calculates the max line length and divides it by the paper width
        to pick the largest possible font size. To print good output from a text
        file, try e.g. `cat foo.txt | fmt -w 40 | fitprint.py`''', prog=prog,)

    argparser.add_argument('src_file', nargs='*',
        help='The filename of a file to print.')

    argparser.add_argument('-e', '--encoding', type=str, default='utf-8',
        help='The encoding to use')

    argparser.add_argument('-w', '--width', type=float, default=72,
        help='Paper width in mm, 72 by default')

    argparser.add_argument('-a', '--aspect', type=float, default=2,
        help='Character h/w aspect ratio')

    argparser.add_argument('-i', '--inches', action='store_true',
        help='Width parameter is in inches')

    argparser.add_argument('-g', '--wiggle', type=float, default=0.001,
        help='Wiggle room; how much of the line-width to ignore;'
        ' generally about 1/1000 = 0.001 is OK. Prevents a sliiiightly too'
        ' large line from wrapping around, leaving one ugly character on'
        ' the next line.')

    args = argparser.parse_args()

    output = partial(fitprint, width=args.width, aspect=args.aspect,
        encoding=args.encoding, wiggle=args.wiggle,
        unit='in' if args.inches else 'mm')

    if len(args.src_file) == 0:
        # use stdin
        # catenate stdinput, parse / render
        src = ''
        src = sys.stdin.buffer.read().decode(args.encoding)
        output(src)
        exit()

    # process each file, respecting encoding, although i really hope nobody
    # ever uses that argument and to be quite frank i haven't tested it

    # path manipulation
    from os import path
    for fname in args.src_file:
        with open(fname, 'r', encoding=args.encoding) as f:
            output(f.read())

if __name__ == '__main__': main()
