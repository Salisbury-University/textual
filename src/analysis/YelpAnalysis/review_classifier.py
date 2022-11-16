#import tensorflow as tf
#import numpy as np
import string
import re
import glob
from tensorflow.keras.layers import TextVectorization
#from tensorflow.keras import layers
#from tensorflow.keras import losses
#from tensorflow.keras import metrics

import nltk
from nltk.corpus import stopwords
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, LSTM, Dropout, Activation, Embedding, Bidirectional
import os, json
from pathlib import Path

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))

file_list = (glob.glob("train_dataset/*/*.txt"))

reviews=[]
labels=[]

vocab=5000
embedding_dim=64
max_length=200
trunc_type = "post"
padding_type = "post"
oov_tok = "<oov>" # OUT OF VOCAB
training_portion = 0.8
i = 0

for input_file in file_list:
    new_file = open(input_file)
    text = new_file.read()

    reviews.append(text)

    rating = input_file
    rating = re.sub("train_dataset/star_", "", rating)
    rating = re.sub("/.*", "", rating)

    labels.append(rating)
    print(str(i) + " " + rating)
    i = i + 1

print(reviews[5])
print(labels[5])
