
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: jupyter_notebooks/Test_module.ipynb

import numpy as np
import pandas as pd
import os
import json
import random

from fastai.text import *
from fastai import *

class Interface():
    def __init__(self, path, bs=64, eval_mode=False):
        '''
        path must be a valid file path or file paths
        path can be either str or Path obj
        eval_mode set to False means create language model
            and general classfier from scratch
        '''
        if not isinstance(path,(list,tuple)):
            path = self._listify(path)     #if things are not iteratorable
        self.path = self._clean_non_json_path(path) #remove non .json paths
        self.csv_path = None
        self.bs = bs
        self.language_model_data = None
        self.classification_model_data = None
        self.eval_mode = eval_mode
        self.df_train, self.df_valid = None, None

    def _clean_non_json_path(self,path):
        filenames = []
        for file_path in path:
            file_extension = file_path.name.split('.')
            if len(file_extension) < 2: continue
            else:
                if file_path.name.split('.')[1] == 'json':
                    filenames.append(file_path)
        return filenames

    def _listify(self,p):
        '''Trun everying in p to a Path object'''

        if p is None: p = []
        elif isinstance(p,str): p = [p]
        else:
            if not isinstance(p,Iterable): p = [p]
        return [Path(i) for i in p]

    def _check_data_format(self):
        if self.path == []: return False
        one_file = self.path[0]
        flag = 0
        with open(one_file) as f:
            data = json.load(f)
        basilica_keys = ['data_points', 'num_data_points', 'id']
        baslilca_data_keys = ['body', 'label', 'source', 'embedding']
        for key in basilica_keys:
            if not key in data.keys(): flag +=1
        for key in baslilca_data_keys:
            if not key in data['data_points'][0].keys(): flag +=1 #only check the first item...
        if flag != 0:
            print('Warning: data source not from Basilica, exit...')
            return False
        return True

    def _convert_json_to_csv(self,test=False):
        #use self.path to grab json format Basilica data
        #return csv file
        #body,label,source
        body, label, source = [], [], []
        for one_file_path in self.path:
            with open(one_file_path) as file:
                data = json.load(file)
            for item in data['data_points']:
                body.append(item['body'])
                label.append(item['label'])
                source.append(item['source'])
            df = pd.DataFrame(list(zip(body, label, source)),
                             columns = ['Body', 'Label', 'Source'])

            #check if the parent directory exists
            if test:
                if not os.path.exists(one_file_path.parent/'delete_test'):
                    os.makedirs(one_file_path.parent/'delete_test')
            else:
                if not os.path.exists(one_file_path.parent/'csv'):
                    os.makedirs(one_file_path.parent/'csv')

            if test: dest = one_file_path.parent/'delete_test'
            else: dest = one_file_path.parent/'csv'
            filename = Path(one_file_path.name).stem + '.csv'
            df.to_csv(dest/filename,index=False)
            print(f'convert {filename} to csv')
        self.csv_path = dest

    def _prepare_df(self):
        dfs = []
        for file in self.csv_path.ls():
            df = pd.read_csv(file)
            dfs.append(df)
        return pd.concat(dfs)

    def _train_valid_split(self,total_filenames,train_pct=0.7):
        '''split the train and test base on total datasets
            return train_list and valid_list with their associated path'''
        total_filenames = total_filenames.ls()
        random.seed(42)
        random.shuffle(total_filenames)

        split_point = round(len(total_filenames)*train_pct)
        assert (type(split_point) == int)
        self.df_train, self.df_valid = total_filenames[:split_point],total_filenames[split_point:]

    def pre_processing(self,skip_convert_json=False,test=False):
        if not self._check_data_format(): exit(0) #we can't handle non Basilica data
        if not skip_convert_json: self._convert_json_to_csv(test)
        if self.eval_mode:
            #TODO: set data_lm_path
            #      load data_lm vocab
            #      create individual classification data bunch using data_lm vocab
            pass
        else:
            '''
            Getting language model data bunch
            Split general classifier train and valid
            '''
            df_total = self._prepare_df()
            #Spacy Tokenization,pre_rules, post_rules applied,Numericalization
            #create fastai databunch, which is a pair of train, valid dataloader of Pytorch
            self.language_model_data = (TextList
                                        .from_df(df_total,path=path)
                                        .split_by_rand_pct(0.1)
                                        .label_for_lm()
                                        .databunch(bs=self.bs,num_workers=16)
                                        )
            #Split data for general classifier
            self._train_valid_split(self.csv_path)


