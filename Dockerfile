FROM continuumio/miniconda3

RUN conda create -n nlp_model_gen python=3.6
ENV PATH /opt/conda/envs/nlp_model_gen/bin:$PATH

RUN git clone https://github.com/heye0507/individualNLPClassifier.git

WORKDIR /individualNLPClassifier
RUN conda install --name nlp_model_gen --file environment.txt
 


