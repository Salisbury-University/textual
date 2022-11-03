#TextAnalysisFuncts.py

import spacy
#import re <-- might not be needed but leaving it here just incase
import sklearn
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# This Function creates a list of 3 tuples containing sentence, its determined sentiment, and the order it appears in text.
def SentimentAnalysis(text):
    #create the nlp object
    nlp = spacy.load("en_core_web_sm")

    #add suffix rules to the tokenizer in our nlp object to seperate wikipedia in-text citations:
    suffixes = nlp.Defaults.suffixes + [r"[\.\,\?\!\:\;\'\"\}]"] + [r"\[\d+\]"]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search

    #turn the text into a SpaCy doc using the nlp
    fullDoc = nlp(text)

    #separate our doc into a tuples of sentences
    sentences = tuple(fullDoc.sents)

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # Where we will store each tuple of data
    sentiments = []
    #This Loop does a sentence by sentence analysis of the text.
    for index, sentence in enumerate(sentences, 1):

        # polarity_scores is a method of SentimentIntensityAnalyzer
        # object gives a sentiment dictionary.
        # which contains pos, neg, neu, and compound scores.
        
        sentiment_dict = sid_obj.polarity_scores(sentence.text)
        
        # decide sentiment as positive, negative and neutral and count each sentence based on compound score.
        if sentiment_dict['compound'] >= 0.05 :
            result = "pos"
            
        elif sentiment_dict['compound'] <= - 0.05 :
            result = "neg"
            
            
        else :
            result = "neu"

        thisTuple = tuple((sentence.text, result, index))
        sentiments.append(thisTuple)
    
    return sentiments
        

# This Function creates a list of 3 tuples containing words in the text, their part of speech and dependency tags
def TagWords(text):
    #create the nlp object
    nlp = spacy.load("en_core_web_sm")

    #add suffix rules to the tokenizer in our nlp object to seperate wikipedia in-text citations:
    suffixes = nlp.Defaults.suffixes + [r"[\.\,\?\!\:\;\'\"\}]"] + [r"\[\d+\]"]#[r"[\.\,\?\!\:\;\'\"\}]\[\d+\]"]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search

    #turn the text into a doc using the nlp
    fullDoc = nlp(text)

    #separate our document into a list of sentences
    sentences = tuple(fullDoc.sents)

    # Where we will store each tuple of data
    wordTags = []

    # This loops through all sentences in the text.
    for sentence in sentences:
        
        #This loop goes through every word in each sentence
        #Create a 3 tuple for each token which contains each word, its dependency tag and its part of speech tag
        for word in sentence:
            thisTuple = tuple((word.text, word.dep_, word.pos_))
            wordTags = thisTuple
    return wordTags


# This Function creates a list of 2 tuples containing of entities and their label (what type of entity they are)
def getEntities(text):
 

    #create spaCy nlp object
    nlp = spacy.load("en_core_web_sm")

    #add suffix rules to the tokenizer in our nlp object to seperate wikipedia in-text citations as seperate tokens:
    suffixes = nlp.Defaults.suffixes + [r"[\.\,\?\!\:\;\'\"\}]"] + [r"\[\d+\]"]#[r"[\.\,\?\!\:\;\'\"\}]\[\d+\]"]
    suffix_regex = spacy.util.compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_regex.search

    #turn the text into a doc using the nlp object
    fullDoc = nlp(text)
    
    #Where we will store each tuple of data
    entities = []

    for ent in fullDoc.ents:
        thisTuple = tuple((ent.text, ent.label_))
        entities.append(thisTuple)

    return entities

