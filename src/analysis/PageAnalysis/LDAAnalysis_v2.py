# LDAAnalysis_v2.py --> a redone version of the LDA Analysis model. Uses a different
# method of preprocessing in order to get more accurate models. 

import sys
import os
from pymongo import MongoClient
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import * 
import numpy as np
import nltk

nltk.download('wordnet')
np.random.seed(2018) 

# getting authorization from the password file 
def get_credentials():

	with open("mongopassword.txt", "r") as pass_file:
		lines = pass_file.read().splitlines()

	return lines

# returns a reference to the client, used to connect to the database
def get_client():

	lines = get_credentials()
	username = lines[0]
	password = lines[1]

	client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

 	return client

# returns a reference to our specific database
def get_database(client):
	
	return client.textual

# closes the database
def close_database(client):

	client.close()

# lemmatizes the words that are input
# lemmatize essentially means to remove any endings to find the root of the word input
def lemmatize_stemming(text_input): 
    
	return stemmer.stem(WordNetLemmatizer().lemmatize(text_input, pos='v'))

# preprocesses the text (removes stop words and words shorter than 3 letters) 
def preprocess(text_input): 
	
	# adding more stopwords that tend to appear in the documents

	stopwords = gensim.parsing.preprocessing.STOPWORDS.union(set(['https', 'http', 'reddit', 'thread', 'post', 'wiki', 'search', 'like', 'removed', 'deleted']))

	# creates a list of preprocessed tokens if they are not in the stop words and are longer than 2 letters
	preprocessed_results = [token for token in gensim.utils.simple_preprocess(text_input) if token not in \
	stopwords and len(token) > 3] 

	return preprocessed_results 

# creates the dictionary and BOW, prints words if specified
def get_dictionary_BOW(processed_documents, print_words=False):

	dictionary = (gensim.corpora.Dictionary(processed_documents)).filter_extremes(no_below=15, no_above=0.5, keep_n=100000) 
    
	bow_corpus = [dictionary.doc2bow(doc) for doc in processed_documents] 

	if print_words: 

		for doc in bow_corpus:

			for i in range(len(doc)):

				print(f'Word: {doc[i][0]} ("{dictionary[doc[i][0]]}") appears {doc[i][1]} time(s).')

	return dictionary, bow_corpus 

if __name__ == "__main__": 

    pass
 
