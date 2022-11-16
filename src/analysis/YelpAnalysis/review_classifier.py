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

reviews = []
labels = []

vocab=5000
embedding_dim=64
max_length=500
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

    new_file.close()
    labels.append(rating)
    print(str(i) + " " + rating)
    i = i + 1

train_size = int(len(reviews) * training_portion)

train_reviews = reviews[0: train_size]
train_labels = labels[0: train_size]

validation_reviews = reviews[train_size:]
validation_labels = labels[train_size:]

print("Tokenizing")
tokenizer = Tokenizer(num_words = vocab, oov_token=oov_tok)
tokenizer.fit_on_texts(train_reviews)
word_index = tokenizer.word_index

print("Extracting sequences")
train_sequences = tokenizer.texts_to_sequences(train_reviews)
train_padded = pad_sequences(train_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

validation_sequences = tokenizer.texts_to_sequences(validation_reviews)
validation_padded = pad_sequences(validation_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

label_tokenizer = Tokenizer()
label_tokenizer.fit_on_texts(labels)

training_label_seq = np.array(label_tokenizer.texts_to_sequences(train_labels))
validation_label_seq = np.array(label_tokenizer.texts_to_sequences(validation_labels))

print("Creating Model")
model = Sequential()

model.add(Embedding(vocab, embedding_dim))
model.add(Dropout(0.5))
model.add(Bidirectional(LSTM(embedding_dim)))
model.add(Dense(5, activation="softmax"))

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

num_epochs = 12
history = model.fit(train_padded, training_label_seq, epochs=num_epochs, validation_data=(validation_padded, validation_label_seq), verbose=2)
