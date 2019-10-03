#! /usr/bin/env python3
# coding: utf-8

from uti.trainer import *
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Using pre-trained classifier to build individual classifier'
    )

    parser.add_argument(
        '--input-file',
        dest="input_file",
        type=str,
        help="Basilica json file, single file or directory"
    )

    args = parser.parse_args()
    output_filepath = Path(args.input_file).ls()
    print(output_filepath)