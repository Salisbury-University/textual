# Project Name(s): English Contextual Baseline Database
# Program Name: yelp_WordCloud.py
# Date: 03/11/2023
# Description: Reads in the reviews.json file containing a large subset of the Yelp Review data dump and generates visual information explaining details regarding the dataset

# ================================================================================
# Included libraries
# Pandas: storing data
# ================================================================================

import pandas as pd
import collections
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import mpld3

def remove_punc(input_string):
    # Punctuation string
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    cleaned_string = ""

    # If the character is not punctuation append it
    for char in input_string:
        if char not in punc:
            cleaned_string += char

    return cleaned_string

if __name__ == "__main__":    
    # Load csv file, minimize memory usage using chunks
    yelp_review_chunks = pd.read_csv("reviews.csv", chunksize=10000) 

    # Five lists to hold the reviews based on the number of stars
    review_stars = [ [], [], [], [], [] ]

    # 2D list to hold the most common words found in each review
    review_words = [ [], [], [], [], [] ]

    # Stop words
    # List generated by ChatGPT
    stopwords.words("english")

    stop_words = set(stopwords.words("english"))
    stop_words.update(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours', 'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs', 'ive', 'im', 'also'])

    # Iterate through the chunks
    for yelp_review_chunk in yelp_review_chunks:

        # Extract the review text based on the number of stars
        for index, row in yelp_review_chunk.iterrows():
            if (row["stars"] == 5.0):
                review_stars[4].append(row["text"])
            elif (row["stars"] == 4.0):
                review_stars[3].append(row["text"])
            elif (row["stars"] == 3.0):
                review_stars[2].append(row["text"])
            elif (row["stars"] == 2.0):
                review_stars[1].append(row["text"])
            else:
                review_stars[0].append(row["text"])
        
    for i in range(len(review_stars)): 
        # Count the occurence of each word
        num_words = collections.Counter(word.lower() for word in remove_punc(" ".join(review_stars[i])).split() if word.lower() not in stop_words)
        most_common = num_words.most_common(35)
        
        for word, freq in most_common:
            # Append the word for the number of occurrences
            for count in range(freq):
                review_words[i].append(word)

    # Print the lists
    """ 
    for i in range(len(review_words)):
        print("The 25 most common words in " + str(i + 1) + " star reviews are: ")
        for word in review_words[i]:
            print(word, end=" ")
    
        print()
    """

    # Specify graph parameters for each set of words
    # Colors are chosen such that they are easy to dinstiguish from each other
    # Colors and corresponding ASCII values are as follows:
    # #FF5733 (Orange)
    # #F1C40F (Yellow)
    # #1ABC9C (Turquoise)
    # #3498DB (Blue)
    # #9B59B6 (Purple)
    
    color_list = ["#FF5733", "#F1C40F", "#1ABC9C", "#3498DB", "#9B59B6"]

    figure, axs = plt.subplots(nrows=1, ncols=5, figsize=(15, 10))

    # Generate graph for each review category
    for i in range(len(review_words)):
        # Initialize graph
        review_words_graph = WordCloud(width = 1024, height = 1024, background_color = "white", collocations=False)
        
        # Create graph using string (Convert from list of words to single string using .join)
        review_words_graph.generate_from_text(" ".join(review_words[i]))
        
        # Change WordCloud display color
        axs[i].imshow(review_words_graph.recolor(color_func = lambda *args, **kwargs: color_list[i]), interpolation = "bilinear")
        axs[i].axis("off")
        axs[i].set_title("Yelp {} star reviews".format(i+1))

    # Save the figure in HTML format
    html_str = mpld3.fig_to_html(figure)
    Html_file= open("WordCloud.html","w")
    Html_file.write(html_str)
    Html_file.close()

    # Display complete graph
    plt.savefig("YelpWordClouds.png")
    plt.show()
    
    print("Script done...")
