#!/usr/bin/env python3
"""
Extract the set of minimizers from a sequence file
"""

__author__ = "Fabio Cumbo (fabio.cumbo@gmail.com)"
__version__ = "0.1.0"
__date__ = "Apr 21, 2023"

import argparse as ap
import errno
import gzip
import multiprocessing as mp
import os
import time
from functools import partial
from typing import Dict, Set

from Bio import SeqIO

TOOL_ID = "minimizers"


def read_params():
    p = ap.ArgumentParser(
        prog=TOOL_ID,
        description="Extract the set of minimizers from a sequence file",
        formatter_class=ap.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "-a",
        "--aggregate",
        action="store_true",
        default=False,
        dest="aggregate",
        help="Aggregate record results"
    )
    p.add_argument(
        "-i",
        "--input",
        type=os.path.abspath,
        required=True,
        dest="input",
        help="Path to the input sequence file in fasta format. It can be Gzip compressed",
    )
    p.add_argument(
        "-o",
        "--output",
        type=os.path.abspath,
        dest="output",
        help=(
            "Path to the output file with minimizers. "
            "Results are printed on the stdout if no output is provided"
        )
    )
    p.add_argument(
        "-s",
        "--size",
        type=int,
        required=True,
        dest="size",
        help="Length of the minimizers",
    )
    p.add_argument(
        "-w",
        "--window",
        type=int,
        required=True,
        dest="window",
        help=(
            "Size of the sliding window. "
            "It must be greater than the minimizer size"
        ),
    )
    p.add_argument(
        "-n",
        "--nproc",
        type=int,
        default=1,
        dest="nproc",
        help="Make it parallel",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print messages on the stdout"
    )
    p.add_argument(
        "-v",
        "--version",
        action="version",
        version='"{}" version {} ({})'.format(TOOL_ID, __version__, __date__),
        help='Print the "{}" version and exit'.format(TOOL_ID),
    )
    return p.parse_args()


def openrt(filepath: str, mode: str = "r"):
    """
    Wrapper around "open" and "gzip.open"

    :param filepath:    File path
    :param mode:        Read (r - default) or Write mode (w)
    :return:            A buffer
    """

    return gzip.open(filepath, '{}t'.format(mode)) if filepath.endswith('.gz') else open(filepath, mode)


def load_input(filepath: str) -> Dict[str, str]:
    """
    Load a fasta file

    :param filepath:    Sequence input file
    :return:            A dictionary with the sequence records
    """

    with openrt(filepath) as input_file:
        return {record.id: str(record.seq.upper()) for record in SeqIO.parse(input_file, "fasta")}


def get_minimizers(sequence_id: str, sequence_content: str, kmer_size: int = 4, window_size: int = 5) -> Dict[str, Set[str]]:
    """
    Get the set of minimizers for the input sequence

    :param sequence_id:         Input sequence ID
    :param sequence_content:    The actual sequence
    :param kmer_size:           Size of the minimizers
    :param window_size:         Size of the sliding window
    :return:                    A dictionary with just the set of minimizers indexed by the sequence ID
    """

    # Extract kmers
    kmers = [sequence_content[i:i + kmer_size] for i in range(0, len(sequence_content) - kmer_size + 1, 1)]

    # Define windows
    windows = [kmers[i:i + window_size] for i in range(0, len(kmers) - window_size + 1, 1)]

    # Get minimizers
    minimizers = set([min(window) for window in windows])

    return {sequence_id: minimizers}


def get_minimizers_parallel(
    sequences: Dict[str, str],
    kmer_size: int = 4,
    window_size: int = 5,
    nproc: int = 1,
) -> Dict[str, Set[str]]:
    """
    Process the input sequences in parallel and retrieve their set of minimizers

    :param sequences:   A dictionary with the input sequences indexed by the sequence IDs
    :param kmer_size:   Size of the minimizers
    :param window_size: Size of the sliding window
    :param nproc:       Number of parallel processes
    :return:            A dictionary with the set of minimizers indexed by the sequence IDs
    """

    minimizers = dict()

    get_minimizers_partial = partial(
        get_minimizers,
        kmer_size=kmer_size,
        window_size=window_size
    )

    with mp.Pool(processes=nproc) as pool:
        jobs = [
            pool.apply_async(
                get_minimizers_partial,
                args=(sequence_id, sequences[sequence_id],),
                callback=minimizers.update,
            )
            for sequence_id in sequences
        ]

        for job in jobs:
            job.wait()
    
    return minimizers


def main() -> None:
    args = read_params()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.input)

    if os.path.isfile(args.output):
        raise Exception("The output file already exists!")

    outfolder = os.path.dirname(args.output)

    if not os.path.isdir(outfolder):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), outfolder)

    t0 = time.time()

    if args.verbose:
        print("Loading input file: {}".format(args.input))

    sequences = load_input(args.input)

    args.nproc = len(sequences) if args.nproc > len(sequences) else args.nproc

    if args.verbose:
        print("The input file contains {} records".format(len(sequences)))
        print("Extracting minimizers")

    minimizers = get_minimizers_parallel(
        sequences,
        kmer_size=args.size,
        window_size=args.window,
        nproc=args.nproc,
    )

    if args.aggregate:
        minimizers = set().union(*minimizers.values())

        if args.verbose:
            print("The input file contains {} minimizers".format(len(minimizers)))

    if args.verbose:
        print("Dumping results to {}".format(args.output))
    
    with open(args.output, "w+") as output:
        if isinstance(minimizers, set):
            for mini in minimizers:
                output.write("{}\n".format(mini))
        
        else:
            for record in minimizers:
                for mini in minimizers[record]:
                    output.write("{}\t{}\n".format(record, mini))

    t1 = time.time()

    if args.verbose:
        print("Total elapsed time {}s".format(int(t1 - t0)))


if __name__ == "__main__":
    main()