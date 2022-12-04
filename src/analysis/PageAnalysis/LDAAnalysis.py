# using Latent Dirichlet Allocation for topic analysis
# should honestly work way better than what I was doing before
# requires more user input, but it pulls out the top topic works 

# topic modeling is a method for unsupervised classification of documents
# provides methods for "automatically organizing, understanding, searching,
# and summarizing large electronic archives"
#   overall good for finding hidden thhemes, classifying documents into said themes
#   and organizing the documents based on those themes

import gensim
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import sys
import os
from pymongo import MongoClient
from gensim.test.utils import datapath

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

    results=[]
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            results.append(lemmatize_stemming(token))
    return results

def get_dictionary(processed_docs):

    dictionary = gensim.corpora.Dictionary(processed_docs)
    bag_of_words = [dictionary.doc2bow(doc) for doc in processed_docs]

    return bag_of_words, dictionary

def iterate_in_collection(collection_name, database, entries): 

    processed_entries = []

    for entry in entries:

        processed_entries.append(pre_process(entry))

    results = get_dictionary(processed_entries) 

    lda_model = gensim.models.LdaMulticore(results[0], num_topics = 20, id2word = results[1], passes = 10, workers = 2)

    temp_file = datapath(collection_name+"_model")

    lda_model.save(temp_file)

    for i in range(0, lda_model.num_topics-1):
        print(lda_model.print_topic(i)

    '''
    if collection_name == "RedditPosts":

        processed_entries = []

        for entry in entries:

            processed_entries.append(pre_process(entry))

        results = get_dictionary(processed_entries)

        if temp_file is not None:

            lda_model = gensim.models.LdaMulticore.load(temp_file)
            lda_model.update(results[0]))

            lda_model.save(temp_file) 

        else: 

            lda_model = gensim.models.LdaMulticore(results[0], num_topics = 8, id2word = results[1], passes=10, workers=2)

            temp_file = datapath("model") 
            lda_model.save(temp_file) 

    elif collection_name == "WikiSourceText":

        pass

    elif collection_name == "AmazonReviews":

        pass

    elif collection_name == "RedditComments":

        pass

    elif collection_name == "YelpReviews":

        pass
    
    else: 

        pass

    ''' 
if __name__ == '__main__': 

    # get documents 

    # option one: get data from command line
    '''
    if(len(sys.argv) < 2):
        print("Need path to documents.\n")
        sys.exit()

    original_docs = []
    processed_docs = []

    for filename in os.listdir(sys.argv[1]):
        file_ = os.path.join(sys.argv[1], filename)

        if os.path.isfile(file_):
            with open(file_, 'r') as read_file:
                original_docs.append(read_file.read())


    for doc in original_docs: 
        processed_docs.append(pre_process(doc))

    
    results = get_dictionary(processed_docs)

    lda_model = gensim.models.LdaMulticore(results[0], num_topics = 8, id2word = results[1], passes = 10, workers = 2)
    '''

    # option two: pull data from database???? 

    client = get_client()
    database = get_database(client)

    collections = database.list_collection_names()

    # parallelize --> go through each collection
    # run the LDA on each entry
    # assign the topic words to each item 

    # RedditPosts -> 'selftext'
    # WikiSourceText -> 'title' or 'text'
    # AmazonReviews -> 'review_body'
    # RedditComments -> 'body' 
    # YelpReviews -> 'text' 

    entries = [] 

    for col in collections:
        
        if col == "RedditPosts":

            old_entries = []

            old_entries = database[col].find({}, {'selftext':1, '_id':0})

            for old_entry in old_entries:
                entries.append(old_entry['selftext'])

            iterate_in_collection(col, database, entries)

        elif col == "WikiSourceText":

            old_entries = []

            old_entries = database[col].find({}, {'Text':1, '_id':0})

            for old_entry in old_entries:
                entries.append(old_entry['Text'])

        elif col == "AmazonReviews":

            old_entries = []

            old_entries = database[col].find({}, {'review_body':1, '_id':0})

            for old_entry in old_entries:
                entries.append(old_entry['review_body'])

        elif col == "RedditComments":

            old_entries = []

            old_entries = database[col].find({}, {'body':1, '_id':0})

            for old_entry in old_entries:
                entries.append(old_entry['body'])

        elif col == "YelpReviews":

            old_entries = []

            old_entries = database[col].find({}, {'text':1, '_id':0})

            for old_entry in old_entries:
                entries.append(old_entry['text'])
        
        else:

            pass

