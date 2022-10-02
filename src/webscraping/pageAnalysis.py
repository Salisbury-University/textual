from bs4 import BeautifulSoup
from flashtext import KeywordProcessor
import pandas as pd
import csv 
from nltk.stem.lancaster import LancasterStemmer
import time
import datetime

# inspiration/help:
# https://towardsdatascience.com/industrial-classification-of-websites-by-machine-learning-with-hands-on-python-3761b1b530f1

# keywords for each "category"
# can be changed at any time/fine tuned, but this is just for initial testing.

tech_keywords = ['Computer', 'Storage', 'Technology', 'Business',
'Software', 'Hardware', 'Tech', 'Gadget', 'News', 'Marketing']
hist_keywords = ['Historical', 'Learning', 'Civics', 'History', 'Past',
'Revolutionary', 'Political', 'Archives', 'Archeology', 'Century']
consume_keywords = ['Bought', 'Product', 'New', 'Store', 'Video', 'Article',
'Delivery', 'Shop']
all_keywords = tech_keywords + hist_keywords + consume_keywords

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

    return (float(num_appearing)/float(num_total))*100


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
        if tech_percent >= history_percent and tech_percentage >= consumer_percentage: 
            catgeory = "technology"
        elif history_percent >= technology_percent and history_percent >= consumer_percent: 
            category = "history" 
        elif consumer_percent >= technology_percent and consumer_percent >= history_percent: 
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

		stemmer = LancasterStemmer()

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

		words = [stemmer.stem(word.lower()) for word in words if word not in ignore_words]

    # removes duplicates

		words = list(set(words))
		classes = list(set(words))

		return words, categories, files


# create_tokenized_words_bog() -> creates a list of tokenized words and a bag of words
# parameters -> from the create_words_list() function - words (list of words), categories
#		(list of categories) and files (list of files)
# returns -> a tuple of a list of training data and a list of output data

def create_tokenized_words_bag(words, categories, files): 

		# stemmer

		stemmer = LancasterStemmer()
	
		# lists of training, output, and empty output

		training = []
		output = []
		empty_output = [0] * len(categories)

		# for each of the files

		for single_file in files:
				
				# create the bag

				bag = []
	
				# gather the list of tokenized words
				
				pattern_words = single_file[0]

				# stem each word

				pattern_words = [stemmer.stem(word.lower()) for word in pattern_words] 
				
				# creates the array of the bag of words
				# 	bag of words is a way to represent text data as machine learning algorithms 
				#		can't deal with text directly, it must use numbers

				for word in words:

						if word in pattern_words:
								bag.append(1) 
						else: 
								bag.append(0) 

				# append the bag to the training data

				training.append(bag)
				output_row = list(empty_output) 
				output_row[categories.index(single_file[1])] = 1
				output.append(output_row)

		return training, output
		
	
# sigmoid -> a key neural network functions, returns the a value on the sigmoid curve
# parameters -> a value, x
# returns -> x's place on the sigmoid curve						

def sigmoid(x): 

		return 1/(1+np.exp(-x))


# sigmoid_to_derivative -> converts the sigmoid value to its derivative
# parameters -> sigmoid_out (the output of a sigmoid functions) 
# return -> the value of the derivative

def sigmoid_to_derivative(sigmoid_out):
		
		return sigmoid_out*(1-sigmoid_out)


# clean_sentence -> tokenizes the sentence and stems the words
# parameters -> sentence (a sentence) 
# returns -> returns the list of tokenized, cleaned words  

def clean_sentence(sentence): 
		
		sentence_words = nltk.word_tokenize(sentence) 
		sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]

		return sentence_words


# bag_of_words -> returns an array of the "bag of words", which is a numerical representation
# 	of the data
# parameters -> sentence (a sentence to be looked at) and words (a collection of keywords)
# returns -> an array representation of the bag 

def bag_of_words(sentence, words): 

		sentence_words = clean_sentence(sentence) 

		# preassigns values of zero	
	
		bag = [0]*len(words)

		# if the sentence word matches any value in the words then the bag value is set to 1
	
		for sentence in sentence_words:
				for i, w in enumerate(words): 
						if w == s: 
								bag[i] = 1

		return(np.array(bag)) 


# think -> iterates through the layers of the network, where the bag of words is the first layer, then
# 	you do matrix multiplication of the input and hidden layers, and finally you output the final layer
# parameters -> sentence (a string of words to act as the input), synpase_0, synapse_1
# returns -> the output 

def think(sentence, synapse_0, synpase_1):

		x = bag_of_words(sentence.lower(), words)
		
		# bag of words is first input

		layer_0 = x

		# matrix multiplcation between the first and hidden layers

		layer_1 = sigmoid(np.dot(first, synapse_0)) 

		# the output
		
		layer_2 = sigmoid(np.dot(second, synapse_1))

		return layer_2


# train -> trains the model and dumps the output data in a .json file
# parameters -> training (list of training data), output (list of output data), categories
# 	(list of categories), hidden_neurons, alpha, epochs, drouput, dropout_percentage
# returns -> nothing

def train(training, output, categories, hidden_neurons=10, alpha=1, epochs=1000, dropout=False, dropout_percentage=0.5): 

		print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
	
		# seeds the random values 	

		np.random.seed(1) 

		# assigns last mean error

		last_mean_error = 1

		# randomly assigns weights with a mean of 0 

		synapse_0 = 2*np.random.random((len(training[0]), hidden_neurons)) - 1
		synpase_1 = 2*np.random.random((hidden_neurons, len(categories))) -1 

		p_syn_0_weight_up = np.zeros_like(synapse_0)
		p_syn_1_weight_up = np.zeroes_like(synapse_1) 
	
		syn_0_dir_count = np.zeros_like(synapse_0)
		syn_1_dir_count = np.zeroes_like(synapse_1) 

		# iterating through all epochs

		for j in iter(range(epochs+1)): 
	
				# first layer is the training data; "feeding forward" through layers 0, 1, 2

				layer_0 = training
				layer_1 = sigmoid(np.dot(layer_0, synapse_0))

				# looking at the dropout

				if(dropout):

						layer_1 *= np.random.binomial([np.ones((len(training),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

						layer_2 = sigmoid(np.dot(layer_1, synapse_1))

						# discovers how much you missed the target value 

						layer_2_error = output - layer_2

				# this breaks out after each fifth of the epochs if, at this iteration, the 
				# error is greater than the last error

				if(j%(.2 * epochs) == 0 and j > (.1 * epochs)):
						
						if np.mean(np.abs(layer_2_error)) < last_mean_error: 
					
								print ("Delta after " + str(j) + " iterations: " + str(np.mean(np.abs(layer_2_error))))
						
						else: 

								print("Break: " + np.mean(np.abs(layer_2_error)) + " > " + last_mean_error) 
								break 
				
				# helps determine how far away are you from the target value and in what direction

				layer_2_delta = layer_2_error * sigmoid_to_derivative(layer_2)

				# how much did the layer_1 values contribute to the layer_2 errors
 
				layer_1_error = layer_2_delta.dot(synapse_1.T)

				# helps determine the direction of the target layer_1
	
				layer_1_delta = layer_1_error * sigmoid_to_derivative(layer_1) 

				# weight update

				syn_1_weight_up = (layer_1.T.dot(later_2_delta))
				syn_0_weight_up = (layer_0.T.dot(layer_1_delta))

				if (j > 0): 
				
						syn_0_dir_count += np.abs(((syn_0_weight_up > 0) + 0) - ((p_syn_0_weight_up > 0) + 0))
						syn_1_dir_count += np.abs(((syn_1_weight_up > 0) + 0) - ((p_syn_1_weight_up > 0) + 0))

						synapse_1 += alpha * syn_1_weight_up
						synapse_0 += alpha * syn_0_weight_up

						p_syn_0_weight_update = syn_0_weight_up
						p_syn_1_weight_update = syn_1_weight_up

				# get the date/time and dumps all of that information into a json dump into a json file

				now = datetime.datetime.now()

				synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(), 'datetime': now.strftime("%Y-%m-%d %H:%M"), 'words': words, 'categories': categories}

				synapse_file = 'synapses.json' 

				with open('~/src/webscraping/'+synapse_file, 'w') as out: 
						json.dump(synapse, out, indent=4, sort_keys=True)


if __name__ == "__main__": 

		processed_keywords =  process_keywords(all_keywords, tech_keywords, hist_keywords, consume_keywords)

			



































