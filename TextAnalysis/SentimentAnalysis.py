#SentimentAnalysis.py

# This Program takes in one string and uses parses it using spaCy's nlp object to parse the text and turn it into a spaCy doc.
# The doc object contains a list of tokens containing POS tags. Using these tags the program tries to find a descriptive term (descriptive word 
# or phrases) and a corresponding target (subject noun) that the descriptive term describes. The descriptive word and target are grouped together 
# into a list of "aspects" of the text. Then it uses TextBlob to do sentiment analysis on the descriptive term being described. A Naive Bayes classifier
# is trained beforehand to improve TextBlob's sentiment analysis accuracy. After this analysis, the program adds a 2-tuple sentiment 
# property (polarity[0 - 1] and subjectivity[-1 - 1]) to every aspect with a descriptive term in the list of  # aspects. Finally, the program prints 
# a list of every aspect that has a sentiment property and prints an average value for both the polarity and subjectivity of the entire text.


import spacy
import re
from textblob import TextBlob # Using SpaCyTextBlob might be better
from textblob.classifiers import NaiveBayesClassifier

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

#separate our document into a list of sentences
sentences = list(fullDoc.sents)

aspects = []

# This loops through every sentence and checks for a descriptive term (adjective) in the sentence 
# that describes the target of the sentence (the subject noun). If there is an adverb describing the adjective,
# it is included in the descriptive term. If either cant be found, target and descriptive term
# are left blank. Each set of descriptive term and target is appended into a list of aspects

# problems: May not be able to detect the correct subject noun in the sentence
for sentence in sentences:
    doc = nlp(sentence.text)
    descriptive_term = ""
    target = ""
    for token in doc:
        if token.pos_ == "NOUN" : # increases accuracy but sometimes misses certain nouns -> and token.dep_ == "nsubj":
            target = token.text
        if token.pos_ == "ADJ" and not token.is_stop and not token.is_punct and not token.is_space and not token.is_digit:
            prepend = ""
            for child in token.children:
                if child.pos_ != "ADV":
                    continue
                prepend += child.text + " "
            descriptive_term = prepend + token.text
    aspects.append({"aspect": target, "description": descriptive_term})

#training a NaivesBayesClassifier to improve accuracy in detecting positive and negative descriptive terms
training = [
    #  within these brackets we can list some training data with the syntax:
    #  ("description", "positive/negative")
    # for example:
    # ("very enjoyable time", "positive"),
    # ("unsuccessful strategy", "negative")
    # Since we need a lot of training data, it may be better to read it in from a file
]

# train the classifier used in the next step
c1 = NaiveBayesClassifier(training)

# classify each description with a sentiment using TextBlob with a trained classifier
numSents = 0
for aspect in aspects:
    aspect["sentiment"] = TextBlob(aspect["description"], classifier=c1).sentiment
    if not aspect["aspect"] == "" and not aspect["description"] == "":
        numSents = numSents + 1
        print(aspect)

# count the total sentiment values (both polarity and subjectivity)
pRating = 0
sRating = 0
for aspect in aspects:
    pRating = pRating + aspect["sentiment"].polarity
    sRating = sRating + aspect["sentiment"].subjectivity

# I dont know what to do with these ratings yet but heres a guess:

# Print the average polarity and subjectivity of all complete aspects
pRating = pRating / numSents
sRating = sRating / numSents
print ("The avg polarity rating is about: ", round(pRating, 2))
print ("The avg subjectivity rating is about: ", round(sRating, 2))