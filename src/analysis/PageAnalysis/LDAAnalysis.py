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

if __name__ == '__main__': 

    # get documents 

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

    