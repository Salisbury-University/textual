import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Counters to keep track of positive, negative, and neutral sentiments
pos = 0
neg = 0
neutral = 0

df = pd.read_csv("youtube_dataset.csv")
comments = df['Comment'][:3]

sia = SentimentIntensityAnalyzer()

#This Loop goes through the first 3 comments in the dataset and gives them sentiment ratings.
for i, comment in enumerate(comments, 1):

    # Display the comment     
    print("Comment " + str(i) + ":")
    print(comment) 
    
    # polarity_scores is a method of SentimentIntensityAnalyzer
    # and returns a dictionary containing pos, neg, neu, and compound scores.
    sentiment_dict = sia.polarity_scores(comment)
    
    print("Overall sentiment dictionary is :", sentiment_dict)
    print("Sentence Overall Rated As ")
    
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
    print()

#display the number of sentences rated positive, negative, or neutral
print("positive comments = ", pos, " negative comments = ", neg, " neutral comments = " , neutral)
