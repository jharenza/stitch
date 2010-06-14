# Stitch

Austin Glenn Davis-Richardson
<harekrishna@gmail.com>

Working under Dr. Eric Triplett & Dr. Adriana Giongo

## Description:

Illumina sequencing has the ability to generate "paired ends."
We did an experiment where our paired ends overlapped.
I wrote this script to assemble the overlapping paired ends using BLAST.

## Installation

1. Make sure you have NCBI's BLAST version 2.2.23 or greater.
   Get it here: <ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/>

2. Once in the stitch directory do:
   > $ sudo python setup.py install

3. Stitch should have installed successfully meaning that you can now do this:
   > $ stitch -h
   to display help information

## Usage

Do this:

> $ stitch -i fastqfile1 -j fastqfile2

Where `fastqfile1` is the 5' most and `fastqfile2` is the 3' most.

## Bugs

 - Quality scores of the left (5') most read override those of the right (3') 
   read.
 - Slow, despite threading.
 - Temporary files don't always get deleted, catching `KeyboardInterrupt`s
   in `Pool()` is weird.  Apparently, this is a Python bug.
 - If there are more than one BLAST hits, two of with with equal e-values,
   the hit used to create the contig is chosen at random.  I should come up
   with additional criteria such as length, and whether or not the data makes
   any sense.
 - `Doubleblast` should return a tuple of BLAST hits, then `Stitch` should 
   determine which hit is used based on whatever criteria (`Doubleblast` is
   **only** for parsing `blastn`, **not** processing results!)

## Features

 - Automatically joines overlapping paired ends!
 - **Multithreaded** - Automatically uses all cores on your system!
 - Generates 3 files: `contigs`, duds from `fastqfile1` and duds from
   `fastqfile2`

## Know your rights

Stitch is free and open-source.
See LICENSE (GNU GPL v3)