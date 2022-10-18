#CurrentTextAnalysis.py

# This Program takes in one string and uses parses it using spaCy's nlp object to parse the text and turn it into a spaCy doc.
# The doc object contains a list of tokens determined by spaCy's tokenizer. The Program reads a string of text read from a file of any length.
# It creates a list of all recognized entities and their corresponding entity labels determined by spaCy's NER. The program goes through every token 
# in each sentence creating a List of each token along with its dependency tag and part of speech tag determined by spaCy. It then analyzes the 
# sentiment of each sentence using VADER's SentimentIntensityAnalyzer and rates the sentence as positive, negative, or neutral. 

# Input:
# string containing our text of interest (Currently only tested on wikipedia articles)

# Result:
# The program should create a list of tagged Entities, tagged Tokens(Words/Punctuations), and count the number of positive, 
# neutral, and negative sentences.

# Please note: All lines of code that are commented out in the form:
"""
<lines of code>
"""
# are for testing and debugging.

import spacy
import re
import sklearn
import pandas as pd
from prettytable import PrettyTable
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#create the nlp object
nlp = spacy.load("en_core_web_sm")

#add suffix rules to the tokenizer in our nlp object to seperate wikipedia in-text citations:
suffixes = nlp.Defaults.suffixes + [r"[\.\,\?\!\:\;\'\"\}]"] + [r"\[\d+\]"]#[r"[\.\,\?\!\:\;\'\"\}]\[\d+\]"]
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search

#positive review about cookies from Amazon
positive = "When I was a child many decades ago, an out of state aunt used to send us these every Christmas. I hadn't had them in years when I stumbled across these on Amazon. Same exact container. Same exact delicious cookies! It's so great to know that there are at least a few things in this world that don't change!"

#negative review for lip masks from Amazon
negative = "I bought this product after reading all the good reviews, but i am totally disappointed. The lip mask is thick so it gets all around my pillow when I sleep, and it's not moisturizing. When I wake up my lips feel dry. A total waste of money!! I don't recommend it."

text = positive

#turn the text into a doc using the nlp
fullDoc = nlp(text)

#separate our document into a list of sentences
sentences = list(fullDoc.sents)

# Create a SentimentIntensityAnalyzer object.
sid_obj = SentimentIntensityAnalyzer()

# counters for the number of sentences determined to have
# positive, negative, and neutral sentiments.
pos = 0
neg = 0
neutral = 0

#List to store all tokens, their dependency tags, and pos tags
WordTagList = []

#This Loop does a sentence by sentence analysis of the text.
for sentence in sentences:

    # polarity_scores is a method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
     
    print("Sentence:", sentence.text) 
    

    sentiment_dict = sid_obj.polarity_scores(sentence.text)
    
    print("Overall sentiment dictionary is :", sentiment_dict)
    #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    print("Sentence Overall Rated As", end = " ")
    
    # decide sentiment as positive, negative and neutral and count each sentence based on compound score.
    if sentiment_dict['compound'] >= 0.05 :
        
        
        print("Positive")
        
        pos += 1
    elif sentiment_dict['compound'] <= - 0.05 :
        
        
        print("Negative")
        
        neg += 1
    else :
        
        
        print("Neutral")
        
        neutral += 1

    #This loop goes through every word in each sentence
    #Create a 3 tuple List of all tokens which contains each word, its dependency tag and its part of speech tag
    for word in sentence:
        WordTagList.append({"word": word.text, "dep": word.dep_, "pos": word.pos_})
    
    print()

#display the number of sentences rated positive, negative, or neutral
print()
print("positive sentences = ", pos, " negative sentences = ", neg, " neutral sentences = " , neutral)
print()

print()
print("Named Entities:")
print()


# Create a list of 2 tuple entity objects consisting of entities and their label (what type of entity they are)
# and adds them to a table to display the results
entityList = []
entityTable = PrettyTable(["Entity", "Label", "Label Meaning"])
for ent in fullDoc.ents:
    entityList.append({"entity": ent.text, "entityType": ent.label})
    entityTable.add_row([ent.text, ent.label_, spacy.explain(ent.label_)])

# Display the results if any named entities have been recognized
if entityList == []:
    print("Detected no named entities")
else:
    print(entityTable)

print()
print("Word with Tags:")
print()

#display all tokens and their given dependency and POS tags in a table:
wordTable = PrettyTable(['Word', 'Dep', 'Pos'])
for word in WordTagList:
    wordTable.add_row([word["word"], word["dep"], word["pos"]])
print(wordTable)
