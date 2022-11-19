from tensorflow import keras
import sys
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import glob
import re
import tensorflow as tf
import pickle
from keras.utils import to_categorical
import nltk
import spacy
from nltk.corpus import stopwords
import string
import pandas as pd

model = keras.models.load_model("final_output.h5")

model.summary()

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


nlp = spacy.load('en_core_web_sm',disable=['parser','ner'])
stop = stopwords.words('english')
def cleanData(review):
    lower_case = review.lower() #lower case the text
    lower_case = lower_case.replace(" n't"," not") #correct n't as not
    lower_case = lower_case.replace("."," . ")
    lower_case = ' '.join(word.strip(string.punctuation) for word in lower_case.split()) #remove punctuation
    words = lower_case.split() #split into words
    words = [word for word in words if word.isalpha()] #remove numbers
    split = [apposV2[word] if word in apposV2 else word for word in words] #correct using apposV2 as mentioned above
    split = [appos[word] if word in appos else word for word in split] #correct using appos as mentioned above
    split = [word for word in split if word not in stop] #remove stop words
    reformed = " ".join(split) #join words back to the text
    doc = nlp(reformed)
    reformed = " ".join([token.lemma_ for token in doc]) #lemmatiztion
    return reformed

vocab=72287
max_length=491

#  Clean up review text
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

print(sys.argv[1])
text = cleanData(sys.argv[1])
print(text)

# print(text.head())

# data=[sys.argv[1]]
# text = cleanData(data)

# print(text.head())

text = tokenizer.texts_to_sequences(text)
text = pad_sequences(text, max_length ,padding='post')

pred = model.predict(text)

labels = ["1 star", "2 star", "3 star", "4 star", "5 star"]

print(labels[tf.argmax(tf.argmax(pred, axis=0))])

#pred = to_categorical(pred, 5)
#print(pred)




