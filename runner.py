#! /usr/bin/env python3
# coding: utf-8

from clasi_user.trainer import *
from clasi_user.downloader import *
import os
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
        default=None
    )

    args = parser.parse_args()
    output_filepath = Path(args.input_file).ls()
    test = Interface(output_filepath,eval_mode=True)
    if args.lm_vocab_path:
        test.pre_processing(lm_path=args.lm_vocab_path)
    else:
        print('downloading vocab...')
        path = Path(args.input_file)/'models'
        if not os.path.exists(path):
            os.makedirs(path)
        download_file_from_google_drive(data_lm_large_id,path/'data_lm_large.pkl')
        download_file_from_google_drive(model_id,path/'general-clasifier-0.84.pth')
        test.pre_processing(lm_path=path)
    test_train = Trainer(test,path)
    test_train.train_individual_clasifier()
