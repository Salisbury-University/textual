#SentimentAnalysis2.py

# This Program takes in one string and uses parses it using spaCy's nlp object to parse the text and turn it into a spaCy doc.
# The doc object contains a list of tokens containing POS tags. Using these tags the program tries to find a descriptive term (descriptive word 
# or phrases) and a corresponding target (subject noun) that the descriptive term describes. The descriptive word and target are grouped together 
# into a list of "aspects" of the text. Then it uses TextBlob to do sentiment analysis on the descriptive term being described. A Naive Bayes classifier
# is trained beforehand to improve TextBlob's sentiment analysis accuracy. After this analysis, the program adds a 2-tuple sentiment 
# property (polarity[0 - 1] and subjectivity[-1 - 1]) to every aspect with a descriptive term in the list of  # aspects. Finally, the program prints 
# a list of every aspect that has a sentiment property and prints an average value for both the polarity and subjectivity of the entire text.


import spacy
import re
import sklearn
import pandas as pd

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#create the nlp object
nlp = spacy.load("en_core_web_sm")

#add suffix rules to the tokenizer in our nlp object to seperate wikipedia in-text citations:
suffixes = nlp.Defaults.suffixes + [r"[\.\,\?\!\:\;\'\"\}]"] + [r"\[\d+\]"]#[r"[\.\,\?\!\:\;\'\"\}]\[\d+\]"]
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search

#open and read in our text
with open("wikifull.txt", "r") as f:
    text = f.read()

#turn the text into a doc using the nlp
fullDoc = nlp(text)

entityList = []
for ent in fullDoc.ents:
    print (ent.text, ent.label_, " - ", spacy.explain(ent.label_))
    entityList.append({"entity": ent.text, "label": ent.label})


#separate our document into a list of sentences
sentences = list(fullDoc.sents)

# Create a SentimentIntensityAnalyzer object.
sid_obj = SentimentIntensityAnalyzer()

pos = 0
neg = 0
neutral = 0

for sentence in sentences:
    # polarity_scores is a method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    
    # print("Sentence: ",sentence.text)
    
    sentiment_dict = sid_obj.polarity_scores(sentence.text)
    
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    # print("Sentence Overall Rated As", end = " ")

    

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        #print("Positive")
        pos += 1

    elif sentiment_dict['compound'] <= - 0.05 :
        #print("Negative")
        neg += 1
    else :
        #print("Neutral")
        neutral += 1

    #print()

print("positive sentences = ", pos, " negative sentences = ", neg, " neutral sentences = " , neutral)

"""
doc = nlp(sentence.text)
polarity += doc._.blob.polarity
subjectivity += doc._.blob.subjectivity
    

print("prolarity whole: ", fullDoc._.blob.polarity)
print("subjectivity whole: ",fullDoc._.blob.subjectivity)
"""