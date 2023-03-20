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
import random

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

	''' 
		Collections: 
	
			AmazonReviews: 'review_body'
			PGText: 'text' 
			RedditComments_v2: 'body'
			RedditPosts_v2: 'selftext'
			WikiSourceText: 'Text' 
			YelpReviews: 'text'
			YoutubeComment: 'text'
			YoutubeVideo: 'vidTitle' 
			TwitterTweets: 'tweet' 

	'''

	# dictionary containing the collection names as the key and the name of the attribute holding their data
	# as the value 
	collections = {'AmazonReviews':'review_body', 'PGText':'text', 'RedditComments_v2':'body', \
	'RedditPosts_v2':'selftext', 'WikiSourceText':'Text', 'YelpReviews':'text', 'YoutubeCommment':'text', \
	'YoutubeVideo':'vidTitle', 'TwitterTweets':'tweet'}

	ignore_collections = ['PGHTML', 'WikiSourceHTML']  
 
	# get collection name from command line
	if len(sys.argv) < 2:
		print("Please provide a collection name.")
		sys.exit

	# access database
	client = get_client()
	database = get_database(client)
	all_collections = database.list_collection_names()

	# check to make sure that new collections haven't been added, exits if the case so you can add it to the dict
	for col in all_collections:
		if col not in collections and not in ignore_collections: 
			print(f'New collection added: {col}.') 

	# check to make sure the inputted collection is correct
	if sys.argv[1] not in collections:
		print('Invalid collection.')
		sys.exit

	# get samples from the database in order to train a model; gets around 25% of the data, keeps the indices chosen
	# in order to classify those using the seen_model function rather than the unseen_model one
	initial_entries = database[sys.argv[1]].find({}, {collections[sys.argv[1]:1, '_id':0}) 	
	
	# check to see if entries is empty
	if len(list(initial_entries.clone())) == 0:
		print("No entries in collection.")
		sys.exit

	# clears out any entries that may throw a key error
	checked_entries = [entry[collections[sys.argv[1]]] for entry in initial_entries if collection[sys.argv[1]] in entry] 
 
	# randomly get values for 25% of the length of the collection
	entries_25 = int(len(checked_entries)*.25)
	
	indices = [] 
	
	for i in range(entries_25):
		val = random.randint(0, len(checked_entries)-1)
		while val in indicies:
			val = random.randint(0, len(checked_entries)-1)
		indicies.append(val) 

	# create a list of the entries that will be passed into the model to be trained
	training_data = [entry for entry in checked_entries if checked_entries.index(entry) in indicies] 




