#! /usr/local/bin/python3

import argparse
# stdin
import sys
import subprocess
from functools import partial

from math import ceil

def fitprint(txt, width=72, aspect=2, encoding='utf-8', wiggle=0.001):
    """
    width: mm
    aspect: character height/width aspect ratio
    wiggle: wiggle room; how much of the line's width to ignore
    """
    mmtoin = 0.039370079
    lines = txt.splitlines()
    maxlen = len(max(lines, key=lambda k: len(k)))
    inwidth = width * mmtoin
    cpi = maxlen / inwidth / (1 - wiggle)
    lpi = maxlen / inwidth / aspect / (1 - wiggle)
    process = subprocess.Popen(['lp', '-o', 'cpi=' + str(cpi),
        '-o', 'lpi=' + str(lpi)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return process.communicate(input=txt.encode(encoding))

def main():
    prog = 'fitprint'
    global cols

    argparser = argparse.ArgumentParser(
        description='the biggest font',
        prog=prog,
        )

    argparser.add_argument('src_file', nargs='*',
        help='The filename of a file to print.')

    argparser.add_argument('-e', '--encoding', type=str, default='utf-8',
        help='The encoding to use')

    argparser.add_argument('-w', '--width', type=float, default=72,
        help='Paper width in mm, 72 by default')

    argparser.add_argument('-a', '--aspect', type=float, default=2,
        help='Character h/w aspect ratio')

    argparser.add_argument('-i', '--wiggle', type=float, default=0.001,
        help='Wiggle room; how much of the line-width to ignore;'
        ' generally about 1/1000 = 0.001 is OK')

    args = argparser.parse_args()

    output = partial(fitprint, width=args.width, aspect=args.aspect,
        encoding=args.encoding, wiggle=args.wiggle)

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
