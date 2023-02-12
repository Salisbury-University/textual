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

    return [token for token in gensim.utils.simple_preprocess(text) if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3]

    '''
    results=[]
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            results.append(lemmatize_stemming(token))
    return results
    '''

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
    results = get_dictionary(processed_entries) 
    lda_model = gensim.models.LdaMulticore(results[0], num_topics = 100, id2word = results[1], passes = 10, workers = 3)

    temp_file = datapath(collection_name+"_model")
    lda_model.save(temp_file)

    for i in range(0, lda_model.num_topics-1):
        print(lda_model.print_topic(i))

    # dictionary containing all of the words in each topic

    topic_words =  {"Topic_" + str(i): [token for token, score in lda_model.show_topic(i, topn=10)] for i in range(0, lda_model.num_topics)}

    # get documents

    documents = [] 
    key = ''

    if(collection_name == "RedditPosts"):
    
        documents = database[collection_name].find({}, {'selftext':1, '_id':1})
        key = 'selftext'
    
    elif(collection_name == "WikiSourceText"):
        
        documents = database[collection_name].find({}, {'Text':1, '_id':1})
        key = 'Text'

    elif(collection_name == "AmazonReviews"):

        documents = database[collection_name].find({}, {'review_body':1, '_id':1})
        key = 'review_body'

    elif(collection_name == "RedditComments"):
    
        documents = database[collection_name].find({}, {'body':1, '_id':1})
        key = 'body'

    elif(collection_name == "YelpReviews"):

        documents = database[collection_name].find({}, {'text':1, '_id':1})
        key = 'text'

    elif(collection_name == "YoutubeComment"):
        
        documents = database[collection_name].find({}, {'text':1, '_id':1})
        key = 'text'

    elif(collection_name == "YoutubeVideo"):
      
        documents = database[collection_name].find({}, {'vidTitle':1, '_id':1})
        key = 'vidTitle'
    
    else:

        pass
        

    f = open("results.txt", 'w')
    counter = 0

    collection = database[collection_name]

    for doc in documents: 

        id = doc['_id']

        processed = pre_process(doc[key])
        bow = get_single_bow(processed)
        topics = lda_model.get_document_topics(bow, minimum_probability=0.01)

        '''
        topics contains a list of tuples where the first entry correspons to the index
        of the topic word in the model 
        '''
        temp = (0,0)
        for item in topics:
            if item[1] > temp[1]:
                temp = item
            else:
                continue

        unique_document_topics = topic_words[str(temp[0])]
        f.write(f"Document number {counter}: ")
        
        for item in unique_document_topics:
            f.write(item + " ")
        counter+=1

        new_val = {"$set" : {"topic_words": unique_document_topics}}
        query = {'_id':id}

        collection.update_one(query, new_val)

    f.close()
    
if __name__ == '__main__': 

    if(len(sys.argv) < 2):
        print("Please provide a collection name.")
        sys.exit

    client = get_client()
    database = get_database(client)
    collections = database.list_collection_names()

    # RedditPosts -> 'selftext'
    # WikiSourceText -> 'title' or 'text'
    # AmazonReviews -> 'review_body'
    # RedditComments -> 'body' 
    # YelpReviews -> 'text' 
    # YoutubeComment -> 'text'
    # YoutubeVideo -> 'vidTitle' 

    found = 0 
    entries = []

    # checking if the input is in the collection names
    if sys.argv[1] in collections:
        found = 1

    if found: 

        if sys.argv[1] == "RedditPosts":

            old_entries = database[sys.argv[1]].find({}, {'selftext':1, '_id':0})
            entries = [old_entry['selftext'] for old_entry in old_entries]
            iterate_in_collection(sys.argv[1], database, entries)

        elif sys.argv[1] == "WikiSourceText":

            old_entries = database[sys.argv[1]].find({}, {'Text':1, '_id':0})
            entries = [old_entry['Text'] for old_entry in old_entries]
            iterate_in_collection(sys.argv[1], database, entries)

        elif sys.argv[1] == "AmazonReviews":

            old_entries = database[sys.argv[1]].find({}, {'review_body':1, '_id':0})
            entries = [old_entry['review_body'] for old_entry in old_entries if 'review_body' in old_entry]
            iterate_in_collection(sys.argv[1], database, entries)

        elif sys.argv[1] == "RedditComments":

            old_entries = database[sys.argv[1]].find({}, {'body':1, '_id':0})
            entries = [old_entry['body'] for old_entry in old_entries]
            iterate_in_collection(sys.argv[1], database, entries)

        elif sys.argv[1] == "YelpReviews":

            old_entries = database[sys.argv[1]].find({}, {'text':1, '_id':0})
            entries = [old_entry['text'] for old_entry in old_entries]
            iterate_in_collection(sys.argv[1], database, entries)
        
        elif sys.argv[1] == "YoutubeComment":

            old_entries = database[sys.argv[1]].find({}, {'text':1, '_id':0})
            entries = [old_entry['text'] for old_entry in old_entries]
            iterate_in_collection(sys.argv[1], database, entries)

        elif sys.argv[1] == "YoutubeVideo":

            old_entries = database[sys.argv[1]].find({}, {'vidTitle':1, '_id':0})
            entries = [old_entry['vidTitle'] for old_entry in old_entries]
            iterate_in_collection(sys.argv[1], database, entries)

        else:

            pass
