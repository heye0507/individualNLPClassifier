# Individual Level NLP Classifier
Individual level NLP classifier is a consulting project worked with Basilica.ai. Basilica.ai is a B2B startup that providing sentiment as a service for social media companies. The goal is to have individual level classifiers so that companies can sort newly generated social media posts based on individual user interested.

[Here](https://docs.google.com/presentation/d/1sYz4yeRL0rFM4c1ScgJoM6id3RIu6Fh1wfRQ1_rghFA/edit#slide=id.p) are the slides for the project


## Project:

- **clasi_user** : All source code for production within structured directory

- **demo_data** :  Sample data for demo purpose. It is one real dataset from Basilica and removed their feature embedding.

## Setup
Clone repository and update python path
```
git clone https://github.com/heye0507/individualNLPClassifier.git
docker build -t nlp_classifier .
docker run -it nlp_classifier
```


## Demo
Run the following two lines for demo

- Take Basilica dataset(s)
- Using AWD_LSTM pre-trained general classification model, fine tune classification head on new dataset
- Save the Pytorch model for in the designated path
```
source activate nlp_model_gen
python3 runner.py --input-file=demo_data/
```

## Input format
- For individual classification model generation, store all the datasets into demo_data/ or create new folder under /individualNLPClassifier/your_data_folder
- The dataset should be in JSON format
- Each JSON file is an object with the fields id, num_data_points, and data_points. data_points is an array of objects with the fields body, embedding, and source. body is the original text of the message. source is the site the message came from. embedding is the embedding produced language model (For non-Basilica dataset, simply make it empty list [])


