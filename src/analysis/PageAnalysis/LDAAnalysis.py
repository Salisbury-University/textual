# using Latent Dirichlet Allocation for topic analysis
# should honestly work way better than what I was doing before
# requires more user input, but it pulls out the top topic works 

# topic modeling is a method for unsupervised classification of documents
# provides methods for "automatically organizing, understanding, searching,
# and summarizing large electronic archives"
#   overall good for finding hidden thhemes, classifying documents into said themes
#   and organizing the documents based on those themes

# IDEAS
#   train the model, then reiterate through all of the documents to find the most probable
#   topic

from gc import collect
import gensim
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import sys
import os
from pymongo import MongoClient
from gensim.test.utils import datapath
from nltk.corpus import stopwords
from gensim.parsing.preprocessing import STOPWORDS

# Get authoriazation from file
def get_credentials():
    with open("mongopassword.txt", "r") as pass_file:
        # Read each line from the file, splitting on newline
        lines = pass_file.read().splitlines()
    # Close the file and return the list of lines
    pass_file.close()
    return lines

# Connect to the database
def get_client():
    # Needs to be done this way, can't push credentials to github
    # Call the get pass function to open the file and extract the credentials
    lines = get_credentials()

    # Get the username from the file
    username = lines[0]

    # Get the password from the file
    password = lines[1]

    # Set up a new client to the database
    # Using database address and port number
    client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)
    
    # Return the client
    return client

# Get a database from the client
# In this case use the textual database
def get_database(client):
    return client.textual

# Close the connection to the database after data has been written
def close_database(client):
    # Close database connection
    client.close()

def lemmatize_stemming(text):

    stemmer = LancasterStemmer()
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def pre_process(text):

    stopwords = STOPWORDS.union(set(['https', 'http', 'reddit', 'thread', 'post', 'wiki', 'search', 'like', 'removed', 'deleted']))
    return [token for token in gensim.utils.simple_preprocess(text) if token not in stopwords and len(token) > 3]


def get_single_bow(doc):

    dictionary_new = gensim.corpora.Dictionary([doc])
    bag_of_words = dictionary_new.doc2bow(doc)

    return bag_of_words

def get_dictionary(processed_docs):

    dictionary = gensim.corpora.Dictionary(processed_docs)
    bag_of_words = [dictionary.doc2bow(doc) for doc in processed_docs]

    return bag_of_words, dictionary

def iterate_in_collection(collection_name, database, entries): 

	processed_entries = [pre_process(entry) for entry in entries]
	empty_removed = [element for element in processed_entries if element != []]
	results = get_dictionary(empty_removed) 
	lda_model = gensim.models.LdaMulticore(results[0], num_topics = 50, id2word = results[1], passes = 20, workers = 4)
	temp_file = datapath(collection_name+"_model")
	lda_model.save(temp_file)
    
	'''
	for i in range(0, lda_model.num_topics-1):
        	print(lda_model.print_topic(i))
	'''
        
    # dictionary containing all of the words in each topic

	topic_words =  {"Topic_" + str(i): [token for token, score in lda_model.show_topic(i, topn=10)] for i in range(0, lda_model.num_topics)}

    # get documents

	documents = [] 
	key = ''

	if collection_name == "RedditPosts_v3":
    
		documents = database[collection_name].find({}, {'selftext':1, '_id':1})
		key = 'selftext'

	elif collection_name == "RedditComments_v3": 

		documents = database[collection_name].find({}, {'body':1, '_id':1})
		key = 'body' 
    
	elif collection_name == "WikiSourceText":
        
		documents = database[collection_name].find({}, {'Text':1, '_id':1})
		key = 'Text'

	elif collection_name == "AmazonReviews":

		documents = database[collection_name].find({}, {'review_body':1, '_id':1})
		key = 'review_body'

	elif collection_name == "YelpReviews":

		documents = database[collection_name].find({}, {'text':1, '_id':1})
		key = 'text'

	elif collection_name == "YoutubeComment":
        
		documents = database[collection_name].find({}, {'text':1, '_id':1})
		key = 'text'

	elif collection_name == "YoutubeVideo":
      
		documents = database[collection_name].find({}, {'vidTitle':1, '_id':1})
		key = 'vidTitle'

	elif collection_name == "TwitterTweets":
	
		documents = database[collection_name].find({}, {'tweet':1, '_id':1}) 
		key = 'tweet'  	

	else:

		pass
        

	f = open("results.txt", 'w')
	counter = 0

	collection = database[collection_name]

	for doc in documents: 

        	# document ID 
		id = doc['_id']

        	# preprocess the documents to get the LDA model
		processed = pre_process(doc[key])
        
		if processed != []: 
        
			bow = get_single_bow(processed)
			topics = lda_model.get_document_topics(bow, minimum_probability=0.01)

            		#topics contains a list of tuples where the first entry correspons to the index
            		#of the topic word in the model 
            
			temp = (0,0)
			for item in topics:
				if item[1] > temp[1]:
					temp = item
				else:
					continue
            
          		 # gets the unique document topics for each individual document
			unique_document_topics = topic_words["Topic_" + str(temp[0])]

            		# write to ouput file 
			f.write(f"Document number {counter}: ")
			f.write(f'{id}: ')
            
			for item in unique_document_topics:
				f.write(item + " ")
			f.write("\n")

        		# putting the information into the database
			new_val = {"$set" : {"topic_words": unique_document_topics}}
			query = {'_id':id}	
			collection.update_one(query, new_val)
        
		else: 
            
			new_val = {"$set" : {"topic_words": "Not enough information."}}
			query = {'_id':id}
			collection.update_one(query, new_val)
            
		counter+=1

	f.close()
    
if __name__ == '__main__': 

	if(len(sys.argv) < 2):
		print("Please provide a collection name.")
		sys.exit
	
	client = get_client()
	database = get_database(client)
	collections = database.list_collection_names()

    # RedditPosts_v3 -> 'selftext'
    # WikiSourceText -> 'title' or 'text'
    # AmazonReviews -> 'review_body'
    # RedditComments_v3 -> 'body' 
    # YelpReviews -> 'text' 
    # YoutubeComment -> 'text'
    # YoutubeVideo -> 'vidTitle' 
		# TwitterTweets -> 'tweet' 

	found = 0 
	entries = []

    # checking if the input is in the collection names
	if sys.argv[1] in collections:
		found = 1

	if found: 

		if sys.argv[1] == "RedditPosts_v3":

			old_entries = database[sys.argv[1]].find({}, {'selftext':1, '_id':0})
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['selftext'] for old_entry in old_entries if 'selftext' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])

		elif sys.argv[1] == "WikiSourceText":

			old_entries = database[sys.argv[1]].find({}, {'Text':1, '_id':0})
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['Text'] for old_entry in old_entries if 'Text' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])

		elif sys.argv[1] == "AmazonReviews":

			old_entries = database[sys.argv[1]].find({}, {'review_body':1, '_id':0})
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['review_body'] for old_entry in old_entries if 'review_body' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])

		elif sys.argv[1] == "RedditComments_v3":

			old_entries = database[sys.argv[1]].find({}, {'body':1, '_id':0})
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['body'] for old_entry in old_entries if 'body' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])

		elif sys.argv[1] == "YelpReviews":

			old_entries = database[sys.argv[1]].find({}, {'text':1, '_id':0})	
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['text'] for old_entry in old_entries if 'text' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])
        
		elif sys.argv[1] == "YoutubeComment":

			old_entries = database[sys.argv[1]].find({}, {'text':1, '_id':0})
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['text'] for old_entry in old_entries if 'text' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])

		elif sys.argv[1] == "YoutubeVideo":

			old_entries = database[sys.argv[1]].find({}, {'vidTitle':1, '_id':0})
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['vidTitle'] for old_entry in old_entries if 'vidTitle' in old_entry]
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])
		
		elif sys.argv[1] == "TwitterTweets":

			old_entries = database[sys.argv[1].find({}, {'tweet':1, '_id':0})]
			if len(list(old_entries.clone())) == 0: 
				print("No entries in collection.")
				sys.exit
			entries = [old_entry['tweet'] for old_entry in old_entries if 'tweet' in old_entry] 
			iterate_in_collection(sys.argv[1], database, entries[:len(entries)//2])

		else:

			pass
