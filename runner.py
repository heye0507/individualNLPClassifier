#! /usr/bin/env python3
# coding: utf-8

from clasi_user.trainer import *
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Using pre-trained classifier to build individual classifier'
    )

    parser.add_argument(
        '--input-file',
        dest="input_file",
        type=str,
        help="The directory Basilica json file(s)"
    )
    
    parser.add_argument(
        '--lm_vocab_path',
        dest="lm_vocab_path",
        type=str,
        help="The directory that contains language data vocab",
        default='/home/jupyter/insight_project/Project-M/data/preprocessed/csv/models'
    )

    args = parser.parse_args()
    output_filepath = Path(args.input_file).ls()
    test = Interface(output_filepath,eval_mode=True)
    test.pre_processing(test=True,lm_path=args.lm_vocab_path)
    test_train = Trainer(test)
    test_train.train_individual_clasifier()