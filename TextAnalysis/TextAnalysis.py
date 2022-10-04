import spacy
import string

#create the nlp object
nlp = spacy.load("en_core_web_md")

#open and read in our text
with open("wiki.txt", "r") as f:
    text = f.read()

#turn the text into a doc using the nlp
doc = nlp(text)
sentences = list(doc.sents)
numOfWords = 0

#Count number of words in the doc
for token in doc:

    #since there are tokens in the doc that do not count as words, such as contractions(ex: "'ve"), possessives (for example "'s"), and
    # punctuation marks (ex: "."), this conditional ensures we only count valid words
    if not (token.is_space or token.is_punct or token.text.startswith("'")):
        #print(token) <- for testing detected tokens
        numOfWords = numOfWords + 1

#calculate estimated average number of words per sentence in text
avg = numOfWords / len(sentences)

#print the total number of tokens in the doc 
print("The total number of tokens in the text is: ", numOfWords) 

#print the total number of sentences in the text counted from the list of sentences
print("The total number of sentences in the text is: ", len(sentences)) 

print("The average number of words per sentence is about: ", avg)
