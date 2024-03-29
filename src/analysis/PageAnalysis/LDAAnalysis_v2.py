# Project: Textual Baseline 
# Subset: Page Categorization/Analysis
# Goal of script: to assign "topic words" to all items in every collection in the database. 
# Creator: Caroline Smith

# Necessary imports: 

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
import multiprocessing as mp 

nltk.download('wordnet')
np.random.seed(2018) 

# Gets authorization credentials to access the database
def get_credentials():

	with open("mongopassword.txt", "r") as pass_file:
		lines = pass_file.read().splitlines()

	return lines

# Returns a reference to the client, used to connect to the database
def get_client():

	lines = get_credentials()
	username = lines[0]
	password = lines[1]

	client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

	return client

# Returns a reference to our specific database
def get_database(client):
	
	return client.textual

# Closes the database
def close_database(client):

	client.close()

# Parameters: a string to be lemmatized and stemmed
# Returns: the resultant string
def lemmatize_stemming(text_input):
	 
        # creates a stemmer from the SnowballStemmer class 
	stemmer = SnowballStemmer(language="english")     

        # passes in the text input to the stemmer object 
	return stemmer.stem(WordNetLemmatizer().lemmatize(text_input, pos='v'))


# Parameters: a list of strings to be preprocessed, a parameter to indicate whether the output should be printed
# Return: a list of tokens 
def preprocess(text_input, print_=False): 
	
	# adding more stopwords that tend to appear in the documents --> can be updated with more commonly used tokens
        stopwords = gensim.parsing.preprocessing.STOPWORDS.union(set(['https', 'http', 'reddit', 'thread', 'post', 'wiki', 'search', 'like', 'removed', 'deleted']))

	# creates a list of preprocessed tokens if they are not in the stop words and are longer than 2 letters
        results = []
        for doc in text_input:

            result = [lemmatize_stemming(token) for token in gensim.utils.simple_preprocess(doc) if token not in stopwords and len(token) >= 3]

            results.append(result)

        # removes empty lists
        new_results = [res for res in results if res != []] 

        return new_results 

# Parameters: a list of processed documents, a parameter to indicate whether the output should be printed
# Results: a list containing the dictionary in the first position and the bag of words corpus in the second position
def get_dictionary_BOW(processed_documents, print_words=False):
	
	# creates the dictionary
	dictionary = gensim.corpora.Dictionary(processed_documents)

        # bow corpus
	bow_corpus = [dictionary.doc2bow(doc) for doc in processed_documents] 

	# prints out the amount of times each word appears
	if print_words: 
		for doc in bow_corpus:
			for i in range(len(doc)):
				print(f'Word: {doc[i][0]} ("{dictionary[doc[i][0]]}") appears {doc[i][1]} time(s).')

	return dictionary, bow_corpus 

# Parameters: the bag of words corpus
# Returns: the Term Frequency Inverse Document Frequency model and the corpus for it
def make_TFIDF(bow_corpus, print_values=False):

	tfidf = models.TfidfModel(bow_corpus)
	corpus_tfidf = tfidf[bow_corpus] 

	# prints out the values from the corpus for each of the document
	if print_values: 
		for doc in corpus_tfidf:
			pprint(doc) 

	return tfidf, corpus_tfidf

# Parameters: bag of words corpus, dictionary (returned from get_dictionary_bow()) 
# Returns: LDA model
def lda_bow_model(bow_corpus, dictionary, print_topics=False):

	# creates the model 
	lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=25, id2word=dictionary, passes=2, workers=10)

	if print_topics: 
		for idx, topic in lda_model.print_topics(-1):
			print(f'Topic: {idx} \nWords: {topic}')

	return lda_model 

# Parameters: corpus for the TFIDF, dictionary 
# Returns: LDA Model with TFIDF 
def lda_tfidf_model(corpus_tfidf, dictionary, print_topics=False):
	
	# creates the model
	lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=5) 
	if print_topics: 
		for idx, topic in lda_model_tfidf.print_topics(-1):
			print(f'Topic: {idx} Word: {topic}')
        
        return lda_model_tfidf

# Parameters: bow_corpus, LDA model object, list of seen_documents, list of corresponding IDs
# Returns: nothing
def classify_seen(bow_corpus, model, seen_documents, ids):

	for i in range(len(seen_documents)):
		id_ = ids[i]
		for index, score in sorted(model[bow_corpus[i]], key=lambda tup: -1*tup[1]):
			print(f'ID: {id}\t \nScore: {score}\t \nTopic: {model.print_topic(index, 10)}.')
			break
		print('----------------------------------------------------------------------') 

# classifies seen documents and updates their entry in the database
def update_seen_documents(bow_corpus, model, seen_documents, ids, collection, database, print_=False):
	
	print("************************Seen Documents*****************************")

	# get all of the topics
	
	topic_words = {"Topic_" + str(i): [token for token, score in model.show_topic(i, topn=10)] for i in range(0, model.num_topics)}

	for i in range(len(seen_documents)): 
		
		# get ID
		if i < len(ids) and i < len(bow_corpus):
			_id = ids[i]
		
			topic = ()		

			# get the top topic from the sorted model, ignore the score
			for index, score in sorted(model[bow_corpus[i]], key=lambda tup: -1*tup[1]):
				topic = model.print_topic(index, 10)
				break 
        
			# split up the topics into a list of words
			split_topics = [((item.split("*"))[1]).replace('"', "") for item in topic.split("+")]
        
			if print_:
				print(f'{_id}', end=" ") 
				print(*split_topics)     
				print("-------------------------------------")

			new_val = {"$set" : {"topic_words": split_topics}} 
			query = {'_id': _id} 
			database[collection].update_one(query, new_val) 

# classifies unseen documents
def classify_unseen(dictionary, model, unseen_documents, ids):

    bow_vectors = []
    preprocessed_data = preprocess(unseen_documents)  

    bow_vectors = [dictionary.doc2bow(doc) for doc in preprocessed_data]
    
    for vector in bow_vectors:
        print(vector)
        id_ = ids[i]
        for index, score in sorted(model[vector], key=lambda tup: -1*tup[1]):
            print(f"ID: {id_}\t \nScore: {score}\t \nTopic: {model.print_topic(index, 10)}")
            break
        print('----------------------------------------------------------------------') 

def update_unseen_documents(dictionary, model, unseen_documents, ids, collection, database, print_=False):

        print("***********************Unseen Documents*************************")

        pool = mp.Pool(mp.cpu_count())
        size_chunks = len(unseen_documents)//mp.cpu_count() 
        unseen_doc_chunks = [unseen_documents[x:x+size_chunks] for x in range(0, len(unseen_documents), size_chunks)] 
        processed_unseen_chunks = pool.map(preprocess, [chunk for chunk in unseen_doc_chunks])
        pool.close()

        processed_unseen = [element for subelement in processed_unseen_chunks for element in subelement]

        bow_vectors = [dictionary.doc2bow(doc) for doc in processed_unseen] 

        topic_words = {"Topic_" + str(i): [token for token, score in model.show_topic(i, topn=10)] for i in range(0, model.num_topics)}

        i=0 

        for vector in bow_vectors:

            if i < len(ids): 

                _id = ids[i]
                i += 1

            topic = ()

            for index, score in sorted(model[vector], key=lambda tup: -1*tup[1]):
                topic = model.print_topic(index, 10)
                break		

            # split up the output
            split_topics = [((item.split("*"))[1]).replace('"', "") for item in topic.split("+")]

            if print_:

                print(f'{_id}', end=" ")
                print(*split_topics) 
                print("-------------------------------------") 

            new_val = {"$set" : {"topic_words": split_topics}} 
            query = {'_id': _id} 
            database[collection].update_one(query, new_val) 		 

if __name__ == "__main__": 

        ignore_collections = ['PGHTML', 'WikiSourceHTML']  
 
	# get collection name from command line
        if len(sys.argv) < 2:
            print("Please provide a collection name.")
            sys.exit

	# access database	
        client = get_client()
        database = get_database(client)
        all_collections = database.list_collection_names()


	# check to make sure the inputted collection is correct
        if sys.argv[1] not in all_collections:
            print('Invalid collection.')
            sys.exit

	# get samples from the database in order to train a model; gets around 25% of the data, keeps the indices chosen
	# in order to classify those using the seen_model function rather than the unseen_model one
        initial_entries = database[sys.argv[1]].find({}, {'text':1, '_id':1}) 	
	
	# check to see if entries is empty
        if len(list(initial_entries.clone())) == 0:
            print("No entries in collection.")
            sys.exit

	# clears out any entries that may throw a key error
        checked_entries = [entry['text'] for entry in initial_entries.clone() if 'text' in entry] 

	# randomly get values for 25% of the length of the collection
        entries_25 = int(len(checked_entries)*.25)
	
        indices = [] 
        val = -1
	
        for i in range(entries_25):
            val = random.randint(0, len(checked_entries)-1)
            if val in indices:
                val = random.randint(0, len(checked_entries)-1) 
            indices.append(val) 

	# create a list of the entries that will be passed into the model to be trained
        training_data = [entry for entry in checked_entries if checked_entries.index(entry) in indices] 

	# get the list of none training entries 
        unseen_data = [entry for entry in checked_entries if checked_entries.index(entry) not in indices]  

	# results[0] is the dictionary, results[1] is the bag of words
        # use multiprocessing to speed up the preprocessing 

        pool = mp.Pool(mp.cpu_count())
        size_chunks = len(training_data)//mp.cpu_count() 
        training_data_chunks = [training_data[x:x+size_chunks] for x in range(0, len(training_data), size_chunks)] 
        processed_training_data = pool.map(preprocess, [chunk for chunk in training_data_chunks])
        pool.close()

        processed_training = [element for subelement in processed_training_data for element in subelement]
    
        results = get_dictionary_BOW(processed_training, False) 

	# training the LDA model on the BOW data
        lda_model = lda_bow_model(results[1], results[0], False)

	# classifying seen data
        seen = list(initial_entries.clone())

        # ids because original formatting was not working 
        ids = []
        for entry in seen: 
            if seen.index(entry) in indices:
                ids.append(entry['_id']) 

	#classify_seen(results[1], lda_model, entries_with_id)
        update_seen_documents(results[1], lda_model, training_data, ids, sys.argv[1], database, True)

	# classifying unseen data
        unseen = list(initial_entries.clone())
	
	# list comprehension was not working 
        ids = [] 
        for entry in unseen:
            if unseen.index(entry) not in indices:
                ids.append(entry['_id'])

        #classify_unseen(results[0], lda_model, unseen_data, ids)
        update_unseen_documents(results[0], lda_model, unseen_data, ids, sys.argv[1], database, True)
