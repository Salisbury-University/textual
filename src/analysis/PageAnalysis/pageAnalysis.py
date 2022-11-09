# Project Name(s): English Contextual Basline Database
# Program Name: pageAnalysis.py
# Date: 10/01/22 - 11/03/22
# Description: Neural network to analyze the topic of a provided article.
# Saving format: csv file with the article title and category

# =========================================================================

# Include libraries

from distutils.command.clean import clean
from re import A
from tracemalloc import get_object_traceback
from flashtext import KeywordProcessor
import pandas as pd
from nltk.stem.lancaster import LancasterStemmer
import time
import datetime
import numpy as np
import nltk
import json
import sys
import multiprocessing as mp
from multiprocessing import Pool
import connectDB
from math import e, log
from keywords import tech, hist, advertisement, religion, political, scientific, cultural, nature, economy, government, sports

ERROR_THRESHOLD = 0.2

nltk.download('punkt')

# inspiration/help:
# https://towardsdatascience.com/industrial-classification-of-websites-by-machine-learning-with-hands-on-python-3761b1b530f1

# getting all of the keywords

# clean_keywords() -> takes list of keywords and returns their stemmed version
# parameters -> keywords : a list of keywords 
# returns -> stemmed_keywords

def clean_keywords(keywords): 

	stemmer = LancasterStemmer()

	stemmed_keywords = [stemmer.stem(keyword.lower()) for keyword in keywords]

	return stemmed_keywords

# kind of weird, stems each of the keywords

tech = clean_keywords(tech)
hist = clean_keywords(hist)
advertisement = clean_keywords(advertisement)
religion = clean_keywords(religion)
political = clean_keywords(political)
scientific = clean_keywords(scientific)
cultural = clean_keywords(cultural)
nature = clean_keywords(nature)
economy = clean_keywords(economy)
government = clean_keywords(government)
sports = clean_keywords(sports)

all_keywords = tech + hist + advertisement + religion + political + scientific + cultural + nature + economy + government + sports

# load_samples -> reads in a text file with samples split with ==========
# parameters -> file_name : a file name that can be read
# returns -> a list of the samples

def load_samples(file_name): 

	all_samples = []

	with open(file_name, 'r') as f: 

		text = f.read()

	all_samples = text.split("=========")

	return all_samples


# process_keywords() -> takes in the keywords provided, uses the
#   KeywordProcessor() class from flashtext for later use.  
# parameters -> keywords (list of all keywords), technology_keywords (just
#   technology keywords), history_keywords (just history keywords),
#   consumer_keywords (just consumer keywords)
# returns -> a tuple of keyword processors 0, 1, 2, and 3 representing all
#   keywords, technology, history, and consumer. 

def process_keywords(keywords, tech, hist, ad, reli, poli, sci, cul, nat, eco, gov, sport): 

  # KeywordProcessor() objects to store keywords 

	keyword_processor0 = KeywordProcessor()
	keyword_processor1 = KeywordProcessor()
	keyword_processor2 = KeywordProcessor()
	keyword_processor3 = KeywordProcessor()
	keyword_processor4 = KeywordProcessor()
	keyword_processor5 = KeywordProcessor()
	keyword_processor6 = KeywordProcessor()
	keyword_processor7 = KeywordProcessor()
	keyword_processor8 = KeywordProcessor()
	keyword_processor9 = KeywordProcessor()
	keyword_processor10 = KeywordProcessor()
	keyword_processor11 = KeywordProcessor()

  # each loop assigns the proper keyword to the right objects

	for word in keywords: 
		keyword_processor0.add_keyword(word)

	for word in tech: 
		keyword_processor1.add_keyword(word) 
	
	for word in hist: 
		keyword_processor2.add_keyword(word)
		
	for word in ad:
		keyword_processor3.add_keyword(word)

	for word in reli: 
		keyword_processor4.add_keyword(word)

	for word in poli: 
		keyword_processor5.add_keyword(word)
	
	for word in sci: 
		keyword_processor6.add_keyword(word)

	for word in cul: 
		keyword_processor7.add_keyword(word)

	for word in nat: 
		keyword_processor8.add_keyword(word)
	
	for word in eco: 
		keyword_processor9.add_keyword(word)

	for word in gov: 
		keyword_processor10.add_keyword(word)

	for word in sport:
		keyword_processor11.add_keyword(word)

	keyword_processor_list = []

	# append to a list to return

	keyword_processor_list.append(keyword_processor0)
	keyword_processor_list.append(keyword_processor1)
	keyword_processor_list.append(keyword_processor2)
	keyword_processor_list.append(keyword_processor3)
	keyword_processor_list.append(keyword_processor4)
	keyword_processor_list.append(keyword_processor5)
	keyword_processor_list.append(keyword_processor6)
	keyword_processor_list.append(keyword_processor7)
	keyword_processor_list.append(keyword_processor8)
	keyword_processor_list.append(keyword_processor9)
	keyword_processor_list.append(keyword_processor10)
	keyword_processor_list.append(keyword_processor11)
    
	return keyword_processor_list


# matching_val() -> finds the percentage of matching keywords
# parameters -> num_total (total number of keywords matching), num_appearing
#   (the number of key words from a single class that is appearing) 
# returns -> the percentage of matching keywords

def matching_val(num_total, num_appearing): 

	if(num_total != 0 and num_appearing != 0): 
		return (float(num_appearing)/float(num_total))*100
	else: 
		return 0


# determine_category() -> computes the likely category of each input html
# parameters -> html (a string of html that will be analyzed), keyword_processors for each category
# returns -> the category of the html

def determine_category(html, keyword_processor_list): 

	text = str(html) 

	# extracts the keywords relevant to each catgeory based on the text

	y0 = len(keyword_processor_list[0].extract_keywords(text))
	y1 = len(keyword_processor_list[1].extract_keywords(text))	
	y2 = len(keyword_processor_list[2].extract_keywords(text))
	y3 = len(keyword_processor_list[3].extract_keywords(text))
	y4 = len(keyword_processor_list[4].extract_keywords(text))
	y5 = len(keyword_processor_list[5].extract_keywords(text))
	y6 = len(keyword_processor_list[6].extract_keywords(text))
	y7 = len(keyword_processor_list[7].extract_keywords(text))
	y8 = len(keyword_processor_list[8].extract_keywords(text))
	y9 = len(keyword_processor_list[9].extract_keywords(text))
	y10 = len(keyword_processor_list[10].extract_keywords(text))
	y11 = len(keyword_processor_list[11].extract_keywords(text))

	# list to contain all of the matching percentage values
	
	values = [] 

    # computes the percentage of matching values

	values.append(("tech", float(matching_val(y0, y1))))
	values.append(("hist", float(matching_val(y0, y2))))
	values.append(("ad", float(matching_val(y0, y3))))
	values.append(("reli",  float(matching_val(y0, y4))))
	values.append(("poli",  float(matching_val(y0, y5))))
	values.append(("sci",  float(matching_val(y0, y6))))
	values.append(("cul",  float(matching_val(y0, y7))))
	values.append(("nat",  float(matching_val(y0, y8))))
	values.append(("eco",  float(matching_val(y0, y9))))
	values.append(("gov",  float(matching_val(y0, y10))))
	values.append(("sport", float(matching_val(y0, y11))))

    # if statement to determine the most likely category 

	if y0 == 0: 
		category='None'
	else:     
		temp = 0
		for tup in values: 
			if(tup[1] > temp):
				temp = tup[1]
				max_tup = tup
		category = max_tup[0]
		
	return category


# insert_csv() -> inserts the categorized data in a csv file
# parameters -> categorized_data (the data appears in a list in the format
#   'category', 'source_html')
# returns -> a DataFrame object

def insert_csv(categorized_data): 

	data = pd.DataFrame(categorized_data)
	data.to_csv('categories.csv', index=False, sep=',')

	data.reset_index()
    
	print("Data written to categories.csv")


# clean_data() -> loads and cleans the classified data, removes null values
# parameters -> categorized_file (a path to the csv file that contains the data)
# returns -> cleaned data in a list

def clean_data(categorized_file):

    data = pd.read_csv(categorized_file)
    data = data[pd.notnull(data['source_html'])]
    data = data[data.category != 'None'] 

    return data

# create_training_data() -> creates a dictionary of the training data with the
#   category as the key
# parameters -> data (a list of training data)
# returns -> a dictionary of the training data

def create_training_data(data): 
    
	training_data = []

    # for loop that iterates through the data

	for index, row in data.iterrows(): 
		training_data.append({"category":row['category'], "source_html":row['source_html']})
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
	ignore_words = []
    
    # tokenizes each word in the source html, adds words to the list, adds files
    # to the list, and adds classes to their list
	
	for pattern in training_data: 

		word = nltk.word_tokenize(pattern['source_html'])
		words.extend(word)

		files.append((word, pattern['category']))
				
		if pattern['category'] not in categories:
			categories.append(pattern['category'])
    
    # stems, lowers, and removes duplicates for each word

	words = [stemmer.stem(word.lower()) for word in words if word not in ignore_words]

    # removes duplicates

	words = list(set(words))
	categories = list(set(categories))

	print(len(files), "files")
	print(len(categories), "categories")
	print(len(words), "unique stemmed words")

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

    stemmer = LancasterStemmer()
		
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
			if w == sentence: 
				bag[i] = 1

	return(np.array(bag)) 


# think -> iterates through the layers of the network, where the bag of words is the first layer, then
# 	you do matrix multiplication of the input and hidden layers, and finally you output the final layer
# parameters -> sentence (a string of words to act as the input), synpase_0, synapse_1
# returns -> the output 

def think(sentence, synapse_0, synapse_1, words):

	x = bag_of_words(sentence.lower(), words)
		
	# bag of words is first input

	layer_0 = x

		# matrix multiplcation between the first and hidden layers

	layer_1 = sigmoid(np.dot(layer_0, synapse_0)) 

	# the output
		
	layer_2 = sigmoid(np.dot(layer_1, synapse_1))

	return layer_2


# train -> trains the model and dumps the output data in a .json file
# parameters -> training (list of training data), output (list of output data), categories
# 	(list of categories), hidden_neurons, alpha, epochs, drouput, dropout_percentage
# returns -> nothing

def train(training, output, categories, words, hidden_neurons=10, alpha=1, epochs=1000, dropout=False, dropout_percentage=0.5): 

	print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percentage if dropout else '') )
	
	# seeds the random values 	

	np.random.seed(1) 

	# assigns last mean error

	last_mean_error = 1

	# randomly assigns weights with a mean of 0 

	synapse_0 = 2*np.random.random((len(training[0]), hidden_neurons)) - 1
	synapse_1 = 2*np.random.random((hidden_neurons, len(categories))) -1 

	p_syn_0_weight_up = np.zeros_like(synapse_0)
	p_syn_1_weight_up = np.zeros_like(synapse_1) 
	
	syn_0_dir_count = np.zeros_like(synapse_0)
	syn_1_dir_count = np.zeros_like(synapse_1) 

	# iterating through all epochs

	for j in iter(range(epochs+1)): 
	
				# first layer is the training data; "feeding forward" through layers 0, 1, 2

		layer_0 = training
		layer_1 = sigmoid(np.dot(layer_0, synapse_0))

				# looking at the dropout

		if(dropout):

			layer_1 *= np.random.binomial([np.ones((len(training),hidden_neurons))],1-dropout_percentage)[0] * (1.0/(1-dropout_percentage))

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

		syn_1_weight_up = (layer_1.T.dot(layer_2_delta))
		syn_0_weight_up = (layer_0.T.dot(layer_1_delta))

		if (j > 0): 
				
			syn_0_dir_count += np.abs(((syn_0_weight_up > 0) + 0) - ((p_syn_0_weight_up > 0) + 0))
			syn_1_dir_count += np.abs(((syn_1_weight_up > 0) + 0) - ((p_syn_1_weight_up > 0) + 0))

			synapse_1 += alpha * syn_1_weight_up
			synapse_1 += alpha * syn_0_weight_up

			p_syn_0_weight_up = syn_0_weight_up
			p_syn_1_weight_up = syn_1_weight_up

				# get the date/time and dumps all of that information into a json dump into a json file

			now = datetime.datetime.now()

			synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(), 'datetime': now.strftime("%Y-%m-%d %H:%M"), 'words': words, 'categories': categories}

			synapse_file = 'synapses.json' 

			with open(synapse_file, 'w+') as out: 
				json.dump(synapse, out, indent=4, sort_keys=True)


# load_data -> loads data from the synapse file
# parameters -> synapse_file (a json file containing the training information)
# returns -> synapse, synapse_0, synapse_1

def load_data(synapse_file): 
	
	with open(synapse_file) as data: 
		synapse = json.load(data)
		synapse_0 = np.asarray(synapse['synapse0'])
		synapse_1 = np.asarray(synapse['synapse1'])

	return synapse, synapse_0, synapse_1


# classify() -> tests an input sentence to find its category
# parameter -> sentence (input sentence), synapse_0, synapse_1, words, categories
# returns -> the results

def classify(sentence, synapse_0, synapse_1, words, categories):

	results = think(sentence, synapse_0, synapse_1, words)

	results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
	results.sort(key=lambda x: x[1], reverse=True) 

	print(results)

	result =[[categories[r[0]],r[1]] for r in results]

	counter=0

	if(len(result) > 1): 

		max_list = result[0]

		for i in range(len(result)):
		
			if(result[i][1] < max_list[1]):
		
				max_list = result[i]
				counter = counter + 1
	else: 
			
		return result[0][0]

	if(counter != 0):

		return max_list[0]


def open_file(file_name):
    f = open(file_name, 'r')
    return f


if __name__ == "__main__": 
		
	htmls = []
	categorized_data = []

	# new command line format: 
	#	python3 pageAnalyis.py --test/--train --twitter/--reddit/--gutenberg/--wikisource

	if(len(sys.argv) == 2 and (sys.argv[1] == "--train" or sys.argv[1] == "-t")):

		samples = load_samples('plaintext.txt')
	
		for item in samples:
			htmls.append(item)
			
		processed_keywords_list =  process_keywords(all_keywords, tech, hist, advertisement, religion, political, scientific, cultural, nature, economy, government, sports)

		for text in htmls:
			cat = determine_category(text, processed_keywords_list)
			categorized_data.append({'category': str(cat), 'source_html': str(text)})

		insert_csv(categorized_data)

		training_data = create_training_data(clean_data('categories.csv'))
		words_categories_files = create_words_list(training_data)
		words_categories_files = create_words_list(training_data)
		
		words = words_categories_files[0]
		categories = words_categories_files[1]
		files = words_categories_files[2]

		tokenized_bag = create_tokenized_words_bag(words, categories, files)
		training = tokenized_bag[0]
		output = tokenized_bag[1]		

		# TRAINING

		x = np.array(training)
		y = np.array(output)

		start_time = time.time()

		train(x, y, categories, words, hidden_neurons=20, alpha=0.15, epochs=30000, dropout=True, dropout_percentage=0.1)

		elapsed_time = time.time() - start_time
		print ("processing time:", elapsed_time, "seconds")

	elif(len(sys.argv) == 2 and (sys.argv[1] == "--test" or sys.argv[1] == "-te")):
		
		training_data = create_training_data(clean_data('categories.csv'))
		words_categories_files = create_words_list(training_data)

		#global words_glob
		#global categories_glob

		words = words_categories_files[0]
		categories = words_categories_files[1]
		files = words_categories_files[2] 

		# load file

		loaded_data = load_data('synapses.json')

		synapse = loaded_data[0]
		synapse_0 = loaded_data[1]
		synapse_1 = loaded_data[2]

		# below you can begin testing after training 

		# get a collection of inputs to be classified and then use parallel processing to classify them

		texts_to_classify = [] # loading in some set of texts from the command line
		output_file = open_file("plaintext.txt") 

		all_texts = output_file.read()

		texts_to_classify = all_texts.split("=========")

		print(len(texts_to_classify))

		with Pool() as pool: 

			print("Number of CPUs: ", mp.cpu_count())

			args = []

			# create an iterable list for the starmap functions

			for text in texts_to_classify: 
				args.append((text, synapse_0, synapse_1, words, categories))
			
			# print out all of the results

			for result in pool.starmap(classify, args):
				print(result)

	else: 
		
		print("Unidentified command line arguments. Please use --test or --train")