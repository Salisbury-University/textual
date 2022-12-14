# Project Name(s): English Contextual Baseline Database
# Program Name: review_classifier_training.py
# Date: 11/26/2022
# Description: Reads in the review.csv file, extacts the reviews and their labels, formats them and trains a keras neural network to classify new reviews into different categories of stars
# Saving format: Output is a pickle file that stores the tokenizer and a h5 file storing the network weights

# ================================================================================
# Included libraries
# Pandas: storing data
# JSON: reading json file
# re, spacy, nltk, string: formatting review text
# glob, pickle: loading and saving 
# tensorflow and keras libraries: Neural network layers
# sklearn: data formatting
# ================================================================================

import numpy as np 
import tensorflow as tf
import pandas as pd
import re
import spacy
from nltk.corpus import stopwords
from tensorflow.keras.utils import to_categorical
import string
import glob
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense,Dropout
from tensorflow.keras.layers import Bidirectional,Embedding,Flatten
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# Clean data function, this will take in a DataFrame of reviews and clean each one
def cleanData(reviews):
    # Dictionary containing typos and contractions, these will be used to clean the text
    apposV2 = {
    "are not" : "are not",
    "ca" : "can",
    "could n't" : "could not",
    "did n't" : "did not",
    "does n't" : "does not",
    "do n't" : "do not",
    "had n't" : "had not",
    "has n't" : "has not",
    "have n't" : "have not",
    "he'd" : "he would",
    "he'll" : "he will",
    "he's" : "he is",
    "i'd" : "I would",
    "i'd" : "I had",
    "i'll" : "I will",
    "i'm" : "I am",
    "is n't" : "is not",
    "it's" : "it is",
    "it'll":"it will",
    "i've" : "I have",
    "let's" : "let us",
    "might n't" : "might not",
    "must n't" : "must not",
    "sha" : "shall",
    "she'd" : "she would",
    "she'll" : "she will",
    "she's" : "she is",
    "should n't" : "should not",
    "that's" : "that is",
    "there's" : "there is",
    "they'd" : "they would",
    "they'll" : "they will",
    "they're" : "they are",
    "they've" : "they have",
    "we'd" : "we would",
    "we're" : "we are",
    "were n't" : "were not",
    "we've" : "we have",
    "what'll" : "what will",
    "what're" : "what are",
    "what's" : "what is",
    "what've" : "what have",
    "where's" : "where is",
    "who'd" : "who would",
    "who'll" : "who will",
    "who're" : "who are",
    "who's" : "who is",
    "who've" : "who have",
    "wo" : "will",
    "would n't" : "would not",
    "you'd" : "you would",
    "you'll" : "you will",
    "you're" : "you are",
    "you've" : "you have",
    "'re": " are",
    "was n't": "was not",
    "we'll":"we will",
    "did n't": "did not"
    }

    # Similar to the first dictionary, these will be used to clean the review text
    appos = {
    "aren't" : "are not",
    "can't" : "cannot",
    "couldn't" : "could not",
    "didn't" : "did not",
    "doesn't" : "does not",
    "don't" : "do not",
    "hadn't" : "had not",
    "hasn't" : "has not",
    "haven't" : "have not",
    "he'd" : "he would",
    "he'll" : "he will",
    "he's" : "he is",
    "i'd" : "I would",
    "i'd" : "I had",
    "i'll" : "I will",
    "i'm" : "I am",
    "isn't" : "is not",
    "it's" : "it is",
    "it'll":"it will",
    "i've" : "I have",
    "let's" : "let us",
    "mightn't" : "might not",
    "mustn't" : "must not",
    "shan't" : "shall not",
    "she'd" : "she would",
    "she'll" : "she will",
    "she's" : "she is",
    "shouldn't" : "should not",
    "that's" : "that is",
    "there's" : "there is",
    "they'd" : "they would",
    "they'll" : "they will",
    "they're" : "they are",
    "they've" : "they have",
    "we'd" : "we would",
    "we're" : "we are",
    "weren't" : "were not",
    "we've" : "we have",
    "what'll" : "what will",
    "what're" : "what are",
    "what's" : "what is",
    "what've" : "what have",
    "where's" : "where is",
    "who'd" : "who would",
    "who'll" : "who will",
    "who're" : "who are",
    "who's" : "who is",
    "who've" : "who have",
    "won't" : "will not",
    "wouldn't" : "would not",
    "you'd" : "you would",
    "you'll" : "you will",
    "you're" : "you are",
    "you've" : "you have",
    "'re": " are",
    "wasn't": "was not",
    "we'll":" will",
    "didn't": "did not"
    }
 
    # Load ntlk stopwords, these will be filtered out of the review text
    nlp = spacy.load('en_core_web_sm',disable=['parser','ner'])
    stop = stopwords.words('english')

    # List to hold review text after being cleaned
    all_=[]
    # Iteration variable
    i = 0
    
    # Iterate through each review in the DataFrame
    for review in reviews:
        # Print to the console every 10,000 iterations
        if i % 10000 == 0:
            print(i)
        
        lower_case = review.lower() # Lower case all text
        lower_case = lower_case.replace(" n't"," not") # Correct n't as not (Not can be used better by the network)
        lower_case = lower_case.replace("."," . ") # Add spaces to the end of sentences
        lower_case = ' '.join(word.strip(string.punctuation) for word in lower_case.split()) #remove punctuation
        words = lower_case.split() # Split text into words
        words = [word for word in words if word.isalpha()] # Remove numbers
        split = [apposV2[word] if word in apposV2 else word for word in words] # Correct using apposV2 as mentioned above
        split = [appos[word] if word in appos else word for word in split] # Correct using appos as mentioned above
        split = [word for word in split if word not in stop] # Remove stop words
        reformed = " ".join(split) # Join words back to the text
        doc = nlp(reformed)
        reformed = " ".join([token.lemma_ for token in doc]) # Lemmatiztion
        all_.append(reformed) # Append document to the list
        i = i + 1 # Increase iteration variable
    df_cleaned = pd.DataFrame() # Create new DataFrame
    df_cleaned['clean_reviews'] = all_ # Add list to DataFrame
    return df_cleaned['clean_reviews'] # Return the clean reviews as a DataFrame

# Function to convert labels to categories
def categorize_labels(data):
    # Encode the review stars to values between 0-4 (1 star - 5 stars)
    encoding = {1: 0,
                2: 1,
                3: 2,
                4: 3,
                5: 4
               }
     
    # Convert labels to classification categories
    y = data['stars'].copy()
    y.replace(encoding, inplace=True)
    y = to_categorical(y,5)

    # Return the categorized labels
    return y

# Function to create a new tokenizer and fit it on the cleaned review data
def create_tokenizer(X_train):
    # Create new Tokenizer
    tokenizer = Tokenizer()
    
    # Fit tokenizer on the cleaned review data
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train) # Get sequences from the tokenizer

    # Get the max length of a sentence and size of the vocabulary
    max_length = max([len(x) for x in X_train])
    vocab_size = len(tokenizer.word_index)+1 # Add 1 to account for unknown word
    print("Vocabulary size: {}".format(vocab_size))
    print("Max length of sentence: {}".format(max_length))

    # Pad empty space
    X_train = pad_sequences(X_train, max_length ,padding='post')

    # Save the tokenizer so it can be used for testing later (The same tokenizer must be used to obtain accurate results)
    with open("tokenizer.pickle", "wb") as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Return the padded scentences
    return X_train

# Function to build the network
def build_network(X_train):
    # Define training variables
    embedding_vector_length=32
    num_classes = 5
    
    # Create the model
    model = Sequential()
    model.add(Embedding(vocab_size,embedding_vector_length,input_length=X_train.shape[1]))
    model.add(Bidirectional(LSTM(250,return_sequences=True)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(64,activation='relu'))
    model.add(Dense(32,activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(16,activation='relu'))
    model.add(Dense(num_classes,activation='softmax'))

    # Compile the model using the adam optimizer
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Return the compiled model
    return model

# Function to train the model
def train_network():
    # Callback to prevent the model from overfitting
    callbacks = [EarlyStopping(monitor='val_loss', patience=5),
                 ModelCheckpoint('../model/model.h5', save_best_only=True,
                                 save_weights_only=False)]

    # Train the model on the training data, spliiting to use some data for validation
    history = model.fit(X_train, y_train, validation_split=0.20, 
                    epochs=15, batch_size=256, verbose=1,
                    callbacks=callbacks)

    # Save the model weights so they can be used for testing later
    model.save("final_output.h5")

    # Return the model performance
    return history

# Main function
if __name__ =="__main__":
     # Setup GPU configuration
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.compat.v1.Session(config=config)
    
    # Print message to console to alert user to current state of script
    print("Loading file...")

    # Load in review.csv file and print dataframe header
    data = pd.read_csv('reviews.csv')
    print(data.head())

    # Extract the data X (review text) and labels Y (stars)
    X = data["text"].copy()
    y = data["stars"].copy()

    # Clean all the data X (review text)
    X_cleaned = cleanData(X)
    # Print the head to verify the data was cleaned
    print(X_cleaned.head())

    # Split the data into test and training data
    X_train, X_test, y_train, y_test = train_test_split(X_cleaned, y, stratify=y, random_state=42,test_size=0.1)

    # Construct the neural network
    model = build_network(X_train)

    # Print a model summary
    model.summary()

    # Train the neural network using the cleaned data
    train_network()
