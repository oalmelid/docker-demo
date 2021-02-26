from argparse import ArgumentParser, FileType, Namespace
from functools import reduce
from typing import List

import pyranges as pr


def parse_input_args() -> Namespace:
    parser = ArgumentParser(description=("Take the intersection of a set of bed files"))
    parser.add_argument("bed_files", help="Bed files to be intersected", nargs="+")
    parser.add_argument(
        "output", help="Output file containing intersection", type=FileType("w")
    )
    return parser.parse_args()


def intersect(peaks: List[pr.PyRanges]) -> pr.PyRanges:
    if len(peaks) == 1:
        return peaks[0]
    else:
        return reduce(pr.PyRanges.intersect, peaks)


if __name__ == "__main__":
    args = parse_input_args()

    try:
        peaks = [pr.read_bed(infile) for infile in args.bed_files]
    except FileNotFoundError as e:
        print(f"Failed to import file: {e}")
        exit(1)

    print(f"Intersecting {args.bed_files}")
    intersection = intersect(peaks)
    print(f"Done, writing output to {args.output}")
    intersection.to_bed(args.output)
