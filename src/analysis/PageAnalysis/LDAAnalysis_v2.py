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
from  gensim import corpora, models
from pprint import pprint

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
	
	# creates the dictionary
	dictionary = (gensim.corpora.Dictionary(processed_documents)).filter_extremes(no_below=15, no_above=0.5, keep_n=100000) 
  # bow corpus
	bow_corpus = [dictionary.doc2bow(doc) for doc in processed_documents] 

	# prints out the amount of times each word appears
	if print_words: 

		for doc in bow_corpus:

			for i in range(len(doc)):

				print(f'Word: {doc[i][0]} ("{dictionary[doc[i][0]]}") appears {doc[i][1]} time(s).')

	return dictionary, bow_corpus 

# creates the TFIDF model 
def make_TFIDF(bow_corpus, print_values=False):

	tfidf = models.TfidfModel(bow_corpus)
	corpus_tfidf = tfidf[bow_corpus] 

	# prints out the values from the corpus for each of the document
	if print_values: 
		for doc in corpus_tfidf:
			pprint(doc) 

	return tfidf, corpus_tfidf

# running an LDA using a BOW
def lda_bow_models(bow_corpus, dictionary, print_topics=False):

	# creates the model 
	lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

	if print_topics: 
		for idx, topic in lda_model.print_topics(-1):
    	print(f'Topic: {idx} \nWords: {topic}')

# running an LDA using TF-IDF
def lda_tfidf_model(corpus_tfidf, dictionary, print_topics=False):
	
	# creates the model
	lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=2) 
	if print_topics: 
		for idx, topic in lda_model_tfidf.print_topics(-1):
    	print(f'Topic: {idx} Word: {topic}')

# classifies a previously seen document
def classify_seen(bow_corpus, model, seen_documents):

	for i in range(len(seen_documents)): 
		for index, score in sorted(model[bow_corpus[i]], key=lambda tup: -1*tup[1]):
			print(f'\nScore: {score}\t \nTopic: {model.print_topic(index, 10)}.') 

# classifies unseen documents
def classify_unseen(dictionary, model, unseen_documents): 
	
	bow_vectors = [dictionary.doc2bow(preprocess(doc)) for doc in unseen_documents]

	for vector in bow_vectors:
		for index, score in sorted(model[vector], key=lambda tup: -1*tup[1]):
    	print("Score: {score}\t Topic: {model.print_topic(index, 5)}")

if __name__ == "__main__": 

    pass
 
