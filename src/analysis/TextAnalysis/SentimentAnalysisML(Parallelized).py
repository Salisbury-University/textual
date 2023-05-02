# SentimentAnalysisML.py

import pandas as pd
import multiprocessing as mp
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords 
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import string
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from langdetect import detect 
from mlxtend.plotting import plot_confusion_matrix


def detect_english(str):
    try:
        if detect(str) == "en":
            return "en"
        else:
            return "not_en"
    except:
        return "not_en"

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def remove_stopwords(line):
    # remove stop words to keep only the words that add meaning to the sentence
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(line)
    lemmatizer = WordNetLemmatizer()

    # Lemmetize each meaningful word to make more useful observations

    filtered_sentence = [lemmatizer.lemmatize(w, get_wordnet_pos(tag)) for w, tag in pos_tag(word_tokens) if not w in stop_words]
    
    # get rid of articles and left over contraction tokens
    for w in filtered_sentence:
        if len(w) < 2:
            filtered_sentence.remove(w)

    str = " ".join(filtered_sentence)

    puncts = string.punctuation
    my_punct = puncts.replace("?","").replace("!","").replace(".","")

    for punct in my_punct:
        str = str.replace(punct, "")

    return str

def preprocess(df):
    
    pool = mp.Pool(mp.cpu_count(),)
    results = [pool.apply_async(detect_english, args=(x,), ) for x in df["Comment"].values.flatten()]
    output = [r.get() for r in results]

    # Close the pool and join the processes
    pool.close()
    pool.join()

    # Create a new column with the output
    df["detected_english"] = output
    df = df[df["detected_english"] == "en"]

    # Evaluate sentiment of each comment.
    # Apply VADER's polarity_scores() function to each element of a column in parallel

    pool = mp.Pool(mp.cpu_count(),)
    results = [pool.apply_async(sia.polarity_scores, args=(x,), ) for x in df["Comment"].values.flatten()]
    output = [r.get()["compound"] for r in results]

    # Close the pool and join the processes
    pool.close()
    pool.join()

    # Create a new column with the output
    df["Polarity"] = output

    # Shuffle the rows
    df.sample(frac=1).reset_index(drop=True)

    nltk.download("punkt")
    nltk.download("stopwords")

    # convert all letters to lowercase:
    df['Comment'] = df['Comment'].map(lambda x: x.lower())

    # get rid of trailing whitespace
    df['Comment'] = df['Comment'].map(lambda x: x.strip())

    # Evaluate sentiment of each comment.
    # Apply VADER's polarity_scores() function to each element of a column in parallel

    pool = mp.Pool(mp.cpu_count(),)
    results = [pool.apply_async(remove_stopwords, args=(x,), ) for x in df["Comment"].values.flatten()]
    output = [r.get() for r in results]
    
    # Close the pool and join the processes
    pool.close()
    pool.join()

    # Create a new column with the output
    df["stopwords_removed"] = output

    return df

if __name__ == '__main__':

    pd.options.mode.chained_assignment = None

    # Create SentimentIntensityAnalyzer object
    sia = SentimentIntensityAnalyzer()

    # Read read the first 3 comments from the dataset.
    df = pd.read_csv("youtube_dataset.csv", usecols=["Comment"])
    
    print("Preprocessing...")
    df = preprocess(df)

        # Define Categories based on compound polarity score
    # -1: Negative
    # 0: Neutral
    # 1: Positive

    df['Categorization'] = 0
    df.loc[ df['Polarity'] > 0.05, 'Categorization'] = 1
    df.loc[ df['Polarity'] < -0.05, 'Categorization'] = -1

    # Plot the distribution of sentiments:
    print("Showing the distribution of sentiments")
    counts = df['Categorization'].value_counts()

    frequencies = [counts[-1], counts[0], counts[1]]
    labels = ["negative", "neutral", "positive"]

    # Display Sentiment Distribution in the dataset
    plt.bar(range(len(labels)), frequencies, 1, edgecolor=(0,0,0))
    plt.title("Distribution of Sentiment in the Dataset")     # add a title
    plt.ylabel("frequencies")   # label the y-axis
    
    # label x-axis with movie names at bar centers
    plt.xticks(range(len(labels)), labels)

    for index, value in enumerate(frequencies):
        plt.text(index, value, str(value))
    plt.show()

    print(df["stopwords_removed"], "\n\n")
    print(df["Categorization"])

    # Filtering out non english comments

    print("Splitting Dataset into testing and training set...")
    # Split the dataset into a testing set and a training set
    X_train, X_test, y_train, y_test = train_test_split(df['stopwords_removed'], df['Categorization'], test_size = 0.2, random_state = 15)

    # This is to test on the testing dataset

    print("Vectorizing Data...")
    # Do a Count Vectorizer thing

    vect = CountVectorizer()
    tf_train = vect.fit_transform(X_train)
    tf_test = vect.transform(X_test)

    # print("\nvect vocabulary: ", vect.vocabulary_)

    lr = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=250)
    lr.fit(tf_train,y_train)

    print("Checking Accuracy of score on both datasets")
    # Check accuracy score on both datasets
    print("Accuracy score on training dataset:",lr.score(tf_train,y_train))
    print("Accuracy score on test dataset:", lr.score(tf_test,y_test))
    print()

    print("Making predictions on the test dataset...")
    # Make predictions on the test dataset
    expected = y_test
    predicted = lr.predict(tf_test)

    index_list = expected.index.tolist()

    with open("log.txt", "w", encoding="utf-8") as file:
        for i, index in enumerate(index_list):
            file.write("Comment: " + df.loc[index, 'Comment'] + "\nstopwords removed: " +  df.loc[index, 'stopwords_removed'] + "\nexpected:" + str(expected.values.flatten()[i]) + "\npredicted:" + str(predicted[i]) + "\n\n")

    print("Plotting confusion matrix for the test dataset...")
    #Plot Confusion matrix for the test dataset
    cf = metrics.confusion_matrix(expected,predicted,labels = [1, 0, -1])
    print(cf)

    fig, ax = plot_confusion_matrix(conf_mat = cf, class_names = [1, 0, -1])
    plt.show()

    print("Showing Classification report...")
    # Print classification report
    print(metrics.classification_report(expected, predicted))

    print("Showing F1 Score.")
    # Find F1 Score
    print(metrics.f1_score(expected, predicted, average='macro'))

    # To test your own comments on the model
    while True:
        entry = input("Enter a YouTube comment: ")

        #Lowercase the input and get rid of whitespace
        entry = entry.lower().strip()
        entry = remove_stopwords(entry)
        tf_test = vect.transform([entry])
        predicted = lr.predict(tf_test)

        if(predicted[0] == 1):
            print("Positive")

        elif(predicted[0] == 0):
            print("Neutral")

        elif(predicted[0] == -1):
            print("Negative")
