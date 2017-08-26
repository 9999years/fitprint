# fitprint

PROBLEM: Unix's `lp` is good, but the built-in rasterizer often picks weird font
sizes.

SOLUTION: This repo.

`fitprint` is a utility for printing with `lp` that reads from STDIN / files and
calculates the max line length and divides it by the paper width to pick the
largest possible font size. To print good output from a text file, try e.g. `cat
foo.txt | fmt -w 40 | fitprint.py`

    usage: fitprint [-h] [-e ENCODING] [-w WIDTH] [-a ASPECT] [-i] [-g WIGGLE]
                    [src_file [src_file ...]]

    positional arguments:
      src_file              The filename of a file to print.

    optional arguments:
      -h, --help            show this help message and exit
      -e ENCODING, --encoding ENCODING
                            The encoding to use
      -w WIDTH, --width WIDTH
                            Paper width in mm, 72 by default
      -a ASPECT, --aspect ASPECT
                            Character h/w aspect ratio
      -i, --inches          Width parameter is in inches
      -g WIGGLE, --wiggle WIGGLE
                            Wiggle room; how much of the line-width to ignore;
                            generally about 1/1000 = 0.001 is OK. Prevents a
                            sliiiightly too large line from wrapping around,
                            leaving one ugly character on the next line.
