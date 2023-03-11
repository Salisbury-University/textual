# SentimentAnalysisML.py


import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from matplotlib import pyplot as plt
import string
import time
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from langdetect import detect 
from mlxtend.plotting import plot_confusion_matrix
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

def detect_english(post):
    if detect(post) == 'en':
        return True


def remove_stopwords(line):
    word_tokens = word_tokenize(line)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return " ".join(filtered_sentence)

start_time = time.perf_counter() #This is to time the execution time

# Create SentimentIntensityAnalyzer object
sia = SentimentIntensityAnalyzer()

# Read read the first 3 comments from the dataset.
df = pd.read_csv("youtube_dataset.csv")

print("Preprocessing...")
df["Polarity"] = df['Comment'].apply(lambda x: sia.polarity_scores(x)["compound"])

# Shuffle the rows
df.sample(frac=1).reset_index(drop=True)

# Define Categories based on compound polarity score
# -1: Negative
# 0: Neutral
# 1: Positive

df['Categorization'] = 0

df.loc[ df['Polarity'] > 0.05, 'Categorization'] = 1
df.loc[ df['Polarity'] < -0.05, 'Categorization'] = -1


# Plot the distribution of sentiments:

counts = df['Categorization'].value_counts()

frequencies = [counts[-1], counts[0], counts[1]]
labels = ["negative", "neutral", "positive"]


plt.bar(range(len(labels)), frequencies, 1, edgecolor=(0,0,0))
plt.title("Distribution of Sentiment in the Dataset")     # add a title
plt.ylabel("frequencies")   # label the y-axis
# label x-axis with movie names at bar centers
plt.xticks(range(len(labels)), labels)
plt.show()

nltk.download("punkt")
nltk.download("stopwords")

# convert all letters to lowercase:
df['Comment'] = df['Comment'].apply(lambda x: x.lower())

# get rid of trailing whitespace
df['Comment'] = df['Comment'].apply(lambda x: x.strip())

# create training dataframe
train = df.copy()
train['Comment'] = train['Comment'].apply(lambda x: x.strip())

# remove stop words to keep only the words that add meaning to the sentence
stop_words = set(stopwords.words('english'))

df['stopwords_removed'] = df['Comment'].apply(lambda x : remove_stopwords(x))

print("Splitting Dataset into testing and training set...")
# Split the dataset into a testing set and a training set
X_train, X_test, y_train, y_test = train_test_split(df['stopwords_removed'], df['Categorization'], test_size = 0.2, random_state = 324)


print("Vectorizing Data...")
# Do a Count Vectorizer thing

vect = CountVectorizer()
tf_train = vect.fit_transform(X_train)
tf_test = vect.transform(X_test)

print("\n\nvect vocabulary: ", vect.vocabulary)

lr = LogisticRegression(multi_class='multinomial', solver='lbfgs')
lr.fit(tf_train,y_train)

print("Checking Accuracy of score on both training sets")
# Check accuracy score on both datasets
print("Accuracy score on training dataset:",lr.score(tf_train,y_train))
print("Accuracy score on test dataset:", lr.score(tf_test,y_test))
print()

print("Making predictions on the test dataset...")
# Make predictions on the test dataset
expected = y_test
predicted = lr.predict(tf_test)

print("Plotting confusion matrix for the test dataset...")
#Plot Confusion matrix for the test dataset
cf = metrics.confusion_matrix(expected,predicted,labels = [1, 0,-1])
print(cf)

fig, ax = plot_confusion_matrix(conf_mat = cf, class_names = [1,0,-1])
plt.show()

print("Showing Classification report...")
# Print classification report
print(metrics.classification_report(expected, predicted))

print("Showing F1 Score.")
# Find F1 Score
print(metrics.f1_score(expected, predicted, average='macro'))
print("\n--- %s seconds total ---" % (time.perf_counter() - start_time))