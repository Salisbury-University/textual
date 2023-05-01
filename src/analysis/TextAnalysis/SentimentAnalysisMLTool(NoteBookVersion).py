# SentimentAnalysisML(NotebookVersion).py
# This is the code used for the detailed Jupyter Notebook version of the tutorial.

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords 
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import string
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer #, TfidfVectorizer 
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
    my_puncts = puncts.replace("?","").replace("!","").replace(".","")

    for punct in my_puncts:
        str = str.replace(punct, "")

    return str

def preprocess(df):

    # Use detect_english function to tag english comments and non-english comments
    # Then filter them out.
    df["detected_english"] = df["Comment"].map(detect_english)
    df = df[df["detected_english"] == "en"]

    # Evaluate sentiment of each comment

    # Apply VADER's polarity_scores() function to each element
    df["Polarity"] = df["Comment"].map(lambda x: sia.polarity_scores(x)['compound'])

    # Shuffle the rows
    df.sample(frac=1).reset_index(drop=True)

    # Define Categories based on compound polarity score
    # -1: Negative
    # 0: Neutral
    # 1: Positive

    df['Categorization'] = 0
    df.loc[df['Polarity'] > 0.05, 'Categorization'] = 1
    df.loc[df['Polarity'] < -0.05, 'Categorization'] = -1

    #Download nltk tokenizer and stopwords
    #nltk.download("punkt")
    #nltk.download("stopwords")

    # convert all letters to lowercase:
    df['Comment'] = df['Comment'].map(lambda x: x.lower())

    # get rid of trailing whitespace
    df['Comment'] = df['Comment'].map(lambda x: x.strip())

    # Evaluate sentiment of each comment.
    # Apply VADER's polarity_scores() function to each element of a column in parallel

    df["stopwords_removed"] = df['Comment'].map(remove_stopwords)

    return df

if __name__ == '__main__':
    # Create SentimentIntensityAnalyzer object
    sia = SentimentIntensityAnalyzer()

    # Read read the first 3 comments from the dataset.
    df = pd.read_csv("youtube_dataset.csv", usecols=["Comment"])

    # Preprocess the data
    print("Preprocessing...")
    df = preprocess(df)
    
    # count the frequency of each class
    counts = df['Categorization'].value_counts()
    frequencies = [counts[-1], counts[0], counts[1]]

    # Create labels for the figure
    labels = ["negative", "neutral", "positive"]

    # Display Sentiment Distribution in the dataset
    plt.bar(range(len(labels)), frequencies, 1, edgecolor=(0,0,0))
    plt.title("Distribution of Sentiment in the Dataset")     # add a title
    plt.ylabel("frequencies")   # label the y-axis
    
    # label x-axis with label names at bar centers
    plt.xticks(range(len(labels)), labels)

    for index, value in enumerate(frequencies):
        plt.text(index, value, str(value))
    plt.show()
    
    # Split the dataset into a testing set and a training set
    print("Splitting Dataset into testing and training set...")
    X_train, X_test, y_train, y_test = train_test_split(df['stopwords_removed'], df['Categorization'], test_size = 0.2, random_state = 15)

    # Vectorize the Data
    print("Vectorizing Data...")
    vect = CountVectorizer()
    tf_train = vect.fit_transform(X_train)
    tf_test = vect.transform(X_test)

    print("\nvect vocabulary: ", vect.vocabulary_)

    lr = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=300)
    lr.fit(tf_train,y_train)
    
    # Check accuracy score on both datasets
    print("Checking Accuracy of score on both datasets")
    print("Accuracy score on training dataset:",lr.score(tf_train,y_train))
    print("Accuracy score on test dataset:", lr.score(tf_test,y_test))
    print()

    # Make predictions on the test dataset
    print("Making predictions on the test dataset...")
    expected = y_test
    predicted = lr.predict(tf_test)

    # Create a log file to manually see what is happening
    index_list = expected.index.tolist()
    with open("log.txt", "w", encoding="utf-8") as file:
        for i, index in enumerate(index_list):
            file.write("Comment: " + df.loc[index, 'Comment'] + "\nstopwords removed: " +  df.loc[index, 'stopwords_removed'] + "\nexpected:" + str(expected.values.flatten()[i]) + "\npredicted:" + str(predicted[i]) + "\n\n")
    
    #Plot Confusion matrix for the test dataset
    print("Plotting confusion matrix for the test dataset...")
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

    # If you would like to test the model your own comments
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
