
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: jupyter_notebooks/Test_BERT.ipynb

from PSM_nlp.interface import *
from pytorch_pretrained_bert import BertTokenizer

class FastaiBertTokenizer(BaseTokenizer):
    '''wrapper for fastai tokenizer'''
    def __init__(self, tokenizer, max_seq=128, **kwargs):
        self._pretrained_tokenizer = tokenizer
        self.max_seq_length = max_seq

    def __call__(self,*args,**kwargs):
        return self

    def tokenizer(self,t):
        return ["[CLS]"] + self._pretrained_tokenizer.tokenize(t)[:self.max_seq_length - 2] + ['[SEP]']

class BERT_Interface(Interface):
    def __init__(self,model_tokenizer, path, eval_mode=True, max_seq=128):
        bert_tok = BertTokenizer.from_pretrained(
            model_tokenizer,
        )
        fastai_tokenizer = Tokenizer(tok_func=FastaiBertTokenizer(bert_tok,max_seq=128),
                                     pre_rules=[fix_html],
                                     post_rules=[]
                                    )
        self.fastai_bert_vocab = Vocab(list(bert_tok.vocab.keys()))
        self.processor = [OpenFileProcessor(),
                          TokenizeProcessor(tokenizer=fastai_tokenizer,include_bos=False,include_eos=False),
                          NumericalizeProcessor(vocab=self.fastai_bert_vocab)
                         ]
        super().__init__(path,eval_mode=eval_mode)

    def _get_individual_data(self,filepath):
        df = pd.read_csv(filepath)
        if df.shape[0]*0.7 < self.bs:
            bs = int(df.shape[0]*0.7)
        else: bs=self.bs
        data = (TextList
                .from_df(df=df, path=self.csv_path,cols='Body',
                         vocab=self.fastai_bert_vocab, processor=self.processor)
                .split_by_rand_pct(0.3,seed=42)
                .label_from_df(cols='Label')
                .databunch(bs=bs,num_workers=2)
               )
        return data

    def pre_processing(self,skip_convert_json=False,test=False,**kwargs):
        #if not self._check_data_format(): exit(0) #we can't handle non Basilica data
        if not skip_convert_json: self._convert_json_to_csv(test)
        if self.eval_mode:
            for file in self.csv_path.ls():
                file_extension = Path(file).name.split('.')
                if len(file_extension) < 2 or file_extension[1] != 'csv': continue
                self.data_list.append(self._get_individual_data(file))
                self.dataset_name.append(file_extension[0])
        else:
            print('Warnning: Does not support fine tune BERT language model')
            raise NotImplementedError