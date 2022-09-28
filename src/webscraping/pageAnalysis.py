from bs4 import BeautifulSoup
from flashtext import KeywordProcessor
import pandas as pd
import csv 

# keywords for each "category"
# can be changed at any time/fine tuned, but this is just for initial testing.

technology_keywords = ['Computer', 'Storage', 'Technology', 'Business',
'Software', 'Hardware', 'Tech', 'Gadget', 'News', 'Marketing']
history_keywords = ['Historical', 'Learning', 'Civics', 'History', 'Past',
'Revolutionary', 'Political', 'Archives', 'Archeology', 'Century']
consumer_keywords = ['Bought', 'Product', 'New', 'Store', 'Video', 'Article',
'Delivery', 'Shop']
keywords = technology_keywords + history_keywords + consumer_keywords

# a list to store all of the html files

global htmls
htmls = []                                      

# process_keywords() -> takes in the keywords provided, uses the
#   KeywordProcessor() class from flashtext for later use.  
# parameters -> keywords (list of all keywords), technology_keywords (just
#   technology keywords), history_keywords (just history keywords),
#   consumer_keywords (just consumer keywords)
# returns -> a tuple of keyword processors 0, 1, 2, and 3 representing all
#   keywords, technology, history, and consumer. 

def process_keywords(keywords, technology_keywords, history_keywords,
consumer_keywords): 

    # KeywordProcessor() objects to store keywords 

    keyword_processor0 = KeywordProcessor()
    keyword_processor1 = KeywordProcessor()
    keyword_processor2 = KeywordProcessor()
    keyword_processor3 = KeywordProcessor()

    # each loop assigns the proper keyword to the right objects

    for word in keywords: 
        keyword_processor0.add_keyword(word)

    for word in technology_keywords: 
        keyword_processor1.add_keyword(word) 

    for word in history_keywords: 
        keyword_processor2.add_keyword(word)

    for word in consumer_keywords:
        keyword_processor3.add_keyword(word)
    
    return keyword_processor0, keyword_processor1, keyword_processor2,
    keyword_processor3 


# matching_val() -> finds the percentage of matching keywords
# parameters -> num_total (total number of keywords matching), num_appearing
#   (the number of key words from a single class that is appearing) 
# returns -> the percentage of matching keywords

def matching_val(num_total, num_appearing): 

    return ((float)num_appearing/float(num_total))*100


# determine_category() -> computes the likely category of each input html
# parameters -> html (a string of html that will be analyzed) 
# returns -> the category of the html

def determine_category(html): 

    text = str(html) 

    # extracts the keywords relevant to each catgeory based on the text

    y0 = len(keyword_processor0.extract_keywords(text))
    y1 = len(keyword_processor1.extract_keywords(text))
    y2 = len(keyword_processor2.extract_keywords(text))
    y3 = len(keyword_processor3.extract_keywords(text))

    total_matches = 0 

    # computes the percentage of matching values

    tech_percent = float(matching_val(y0, y1))
    history_percent = float(matching_val(y0, y2))
    consumer_percent = float(matching_val(y0, y3))

    # if statement to determine the most likely category 

    if y0 == 0: 
        category='None'
    else: 
        if tech_percent >= history_percent and tech_percentage >=
        consumer_percentage: 
            catgeory = "technology"
        elif history_percent >= technology_percent and history_percent >=
        consumer_percent: 
            category = "history" 
        elif consumer_percent >= technology_percent and consumer_percent >=
        history_percent: 
            category = "consumer" 

    return category


# insert_csv() -> inserts the categorized data in a csv file
# parameters -> categorized_data (the data appears in a list in the format
#   'category', 'source_html')
# returns -> None

def insert_csv(categorized_data): 

    with open('categories.csv', 'w') as categoryFile: 

        writer = csv.writer(categoryFile)

        writer.writerows(categorized_data)
    
    print("Data writted to categories.csv") 


# clean_data() -> loads and cleans the classified data, removes null values
# parameters -> categorized_file (a path to the csv file that contains the data)
# returns -> cleaned data in a list

def clean_data(categorized_file):

    data = pd.read_csv(categorized_file)
    data = data[pd.notnull(data['tokenized_source'])]
    data = data[data.category != "None"] 

    return data

# create_training_data() -> creates a dictionary of the training data with the
#   category as the key
# parameters -> data (a list of training data)
# returns -> a dictionary of the training data

def create_training_data(data): 
    
    training_data = {}

    # for loop that iterates through the data

    for index, row in data.iterrows(): 
        training_data.append({"category":row['category'], "source_html":['text']})

    return training_data


# create_words_list() -> tokenizes the source_html and appends each word to the
#   words list; it also appends the word and category to the documents file
# parameters -> training_data (a dictionary of the training data) 
# returns -> a tuple of words, categories, and files 

def create_words_list(training_data): 

    words = []
    categories = []
    files = [] 
    ignore_words = ['?', ',', '.', ';', ':']
    
    # tokenizes each word in the source html, adds words to the list, adds files
    # to the list, and adds classes to their list

    for pattern in training_data: 

        word = nltk.word_tokenize(pattern['source_html'])
        words.extend(word)

        files.append((word, pattern['category']))

        if pattern['category'] not in category:
            categories.append(pattern['category'])
    
    # stems, lowers, and removes duplicates for each word

    words = [stemmer.stem(word.lower()) for word in words if word not in
    ignore_words]

    # removes duplicates

    words = list(set(words))
    classes = list(set(words))

    return words, categories, files
