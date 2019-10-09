
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: jupyter_notebooks/Test_BERT_Trainer.ipynb

from uti.bert_interface import *
from uti.trainer import *
from pytorch_pretrained_bert.modeling import BertConfig, BertForSequenceClassification

class BERT_Trainer(Trainer):
    def __init__(self, bert_interface, model='bert-base-uncased', num_labels=2):
        self.model = BertForSequenceClassification.from_pretrained(model, num_labels)
        super().__init__(bert_interface)

    def _create_leaner(self, data):
        learn = Learner(data, self.model,
                        model_dir=self.dest, metrics=[accuracy]
                       )
        if torch.cuda.is_available():
            learn.to_fp16()
        return learn