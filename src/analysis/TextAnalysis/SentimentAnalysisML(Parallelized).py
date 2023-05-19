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
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from langdetect import detect 
from mlxtend.plotting import plot_confusion_matrix

# <--------------------------------------------------------------------->
# This function takes a string as input. (In this case a YouTube Comment)
# 
# Returns True if the detected language is english
# Returns False if the detected language is some non-english language
# 
# If an exception is raised, it is likely because no language could be detected.
# This mostly occurs in comments that are garbage or containing only punctuations or symbols
# so this is used to filter out noisy comments.
# 
# Note: This function sometimes misclassifies the language so there may still be non english or noisy comments even after
# this is called.
# <--------------------------------------------------------------------->
def detect_english(str):
    try:
        if detect(str) == "en":
            return "en"
        else:
            return "not_en"
    except:
        return "not_en"

# <--------------------------------------------------------------------->
# This function takes a string as input. (In this case a treebank part of speech (pos) tag)
#
# This function is used to convert treebank pos tags into the wordnet pos tag format. since the lemmatizer used in 
# the 'remove_stopwords()' function requires the wordnet format to work, this function is crucial.
# The converted tag is returned.
# <--------------------------------------------------------------------->
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

# <--------------------------------------------------------------------->
# This function takes a string as input. (In this case a YouTube Comment)
#
# This function does more than just removing stopwords dispite the name of the function (Name of the function can be modified if needed)

# This function does some of the most important preprocessing steps such as stopword removal, lemmatization, and removing punctuation.
# 
# Returns a string that has been lemmatized, removed of stopwords, and removed of punctuation 
# <--------------------------------------------------------------------->
def remove_stopwords(line):
    # remove stop words to keep only the words that add meaning to the sentence
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(line)
    lemmatizer = WordNetLemmatizer()

    # Lemmetize each token that isn't a stopword to make more useful observations

    filtered_sentence = [lemmatizer.lemmatize(w, get_wordnet_pos(tag)) for w, tag in pos_tag(word_tokens) if not w in stop_words]
    
    # get rid of articles and left over contraction tokens
    for w in filtered_sentence:
        if len(w) < 2:
            filtered_sentence.remove(w)

    # Join remaining tokens together
    str = " ".join(filtered_sentence)

    # Create a string of punctuations we would like to remove
    puncts = string.punctuation

    # Exclude '?', '!', and '.' from removal since they add some context for sentiment of sentences.
    my_puncts = puncts.replace("?","").replace("!","").replace(".","")

    # delete every punctuation except '?', '!', and '.'
    for punct in my_puncts:
        str = str.replace(punct, "")

    return str

# <--------------------------------------------------------------------->
# This function takes a pandas dataframe as input. (In this case the dataframe containing the YouTube Comments)
# 
# This function applies all the preprocessing steps defined above and more to each row of the dataframe.
# 
# Here is the complete list of steps for preprocessing:
# 
# 1. Filter out non-english and noisy/garbage comments
# 2. Apply VADER's polarity_scores() function to each comment to create a new column called "Polarity".
# So that we can get a general idea of the sentiment of each comment.
# 3. Apply remove_stopwords() function defined above to create a new column called "stopwords_removed".
# 4. Shuffle the dataset randomly to prepare the dataset for the testing and training split.
# 
# Returns the resulting dataframe after performing all operations.
# <--------------------------------------------------------------------->
def preprocess(df):
    
    # Use detect_english function to tag english comments and non-english comments
    # Then filter them out.
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

    # Create SentimentIntensityAnalyzer object
    sia = SentimentIntensityAnalyzer()

    # Apply VADER's polarity_scores() function to each element of a column in parallel
    pool = mp.Pool(mp.cpu_count(),)
    results = [pool.apply_async(sia.polarity_scores, args=(x,), ) for x in df["Comment"].values.flatten()]
    output = [r.get()["compound"] for r in results]

    # Close the pool and join the processes
    pool.close()
    pool.join()

    # Create a new column with the output
    df["Polarity"] = output

    # Download nltk tokenizer and stopwords
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

    # Shuffle the rows
    df.sample(frac=1).reset_index(drop=True)

    return df

# Main function
if __name__ == '__main__':

    # Gets rid of warning
    pd.options.mode.chained_assignment = None

    # Read read the first 3 comments from the dataset.
    df = pd.read_csv("youtube_dataset.csv", usecols=["Comment"])
    
    # Begin Preprocessing steps
    print("Preprocessing...")
    df = preprocess(df)

    # Define Categories based on compound polarity score
    # -1: Negative
    # 0: Neutral
    # 1: Positive
    df['Categorization'] = 0
    df.loc[df['Polarity'] > 0.05, 'Categorization'] = 1
    df.loc[df['Polarity'] < -0.05, 'Categorization'] = -1

    # Plot the distribution of sentiments that have been determined by VADER:
    print("Showing the distribution of sentiments that were determined by VADER")
    counts = df['Categorization'].value_counts()

    # Create a list of labels and counts for each respective class (negative, neutral, and positive)
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
    # Split the dataset into a testing set and a training set
    print("Splitting Dataset into testing and training set...")
    X_train, X_test, y_train, y_test = train_test_split(df['stopwords_removed'], df['Categorization'], test_size = 0.2, random_state = 15)

    # Vectorize the data 
    print("Vectorizing Data...")
    vect = CountVectorizer()
    tf_train = vect.fit_transform(X_train)
    tf_test = vect.transform(X_test)

    # Create Multinomial Logistic Regression Model (Since dealing with multiple classes)
    # n_jobs parameter ensures the training process is parallelized using available cpus
    lr = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=250, n_jobs=mp.cpu_count())
    lr.fit(tf_train,y_train)

    # Print accuracy of self and independent tests.
    print("Checking Accuracy of score on both datasets")
    print("Accuracy score on training dataset:",round(lr.score(tf_train,y_train), 2))
    print("Accuracy score on test dataset:", round(lr.score(tf_test,y_test), 2))
    print()

    # Make predictions on the test dataset
    print("Making predictions on the test dataset...")
    expected = y_test
    predicted = lr.predict(tf_test)

    index_list = expected.index.tolist()

    # Creates a log showing each classification for debugging purposes.
    with open("log.txt", "w", encoding="utf-8") as file:
        for i, index in enumerate(index_list):
            file.write("Comment: " + df.loc[index, 'Comment'] + "\nstopwords removed: " +  df.loc[index, 'stopwords_removed'] + "\nexpected:" + str(expected.values.flatten()[i]) + "\npredicted:" + str(predicted[i]) + "\n\n")

    #Plot and Display confusion matrix for the test dataset
    print("Plotting and displaying confusion matrix for the independent test...")
    cf = metrics.confusion_matrix(expected,predicted,labels = [1, 0, -1])
    print(cf)
    print()

    fig, ax = plot_confusion_matrix(conf_mat = cf, class_names = [1, 0, -1])
    plt.show()

    print("Showing Classification report:")
    # Print classification report
    print(metrics.classification_report(expected, predicted))

    # Find F1 Score
    print("Showing F1 Score:")
    print(round(metrics.f1_score(expected, predicted, average='macro'), 2))
    print()
    
    # To test your own comments on the model
    while True:
        entry = input("Enter a YouTube comment for sentiment classification: ")

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
