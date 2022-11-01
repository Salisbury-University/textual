# Project Name(s): English Contextual Baseline Database
# Program Name: readWikiSource.py
# Date: 10/1/2022-10/31/2022
# Description: Collect pages from the WikiSource website using HTTP requests
# Saving format: List of data is written to the MongoDB database

# ================================================================================
# Included libraries
# urllib, requests: used to make HTTP requests
# bs4: used to parse HTML
# threading, multiprocessing, counter: used to run scraper in parallel
# ================================================================================
import urllib.request
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import functools as ft
import multiprocessing as mp
import threading
import pandas as pd
from collections import Counter

#All punctuation characters
from string import punctuation

#Import Regex
import re

# Used to connect to the MongoDB database
from pymongo import MongoClient

#Constant to Random Page
URL="https://en.wikisource.org/wiki/Special:RandomRootpage/Main"

#List of scripts to be removed
inlist = ['[document]',
                'noscript',
                'header',
                'html',
                'meta',
                'head',
                'input',
                'script',
                'style',
                'script',
                'footer']

# Connect to the database
def get_client():
    # Set up a new client to the database
    # Using database address and port number
    client = MongoClient("mongodb://10.251.12.108:30000")

    # Return the client
    return client

# Convert pandas dataframe to dict
def convert_to_dict(dataframe):
    # Convert to dict
    dict_file = dataframe.to_dict('dict')

    # Return dict
    return dict_file

# Get the database, we are using the textual database | hardcoded currently (bad)
def get_database(client):
    return client.textual

# Important, close the database
def close_database(client):
    # Close the connection to the database
    client.close()

#Removes leading and trailing punctuation from a string
def clean_string(input_string):
    #Remove all leading punctuation
    input_string = input_string.lstrip(punctuation)
    #Remove all trailing punctuation
    input_string = input_string.rstrip(punctuation)

    #Return the cleaned string
    return input_string

#Save the HTML content of a page to a separate file
def save_html(html, page_name):
    #Open a file with the name HTML_'name of page'.txt
    str = "HTML_" + page_name + ".html"
    file = open_file(str)
    
    #Write to the output file and close it
    file.writelines(html)
    file.close()

#Get the metadata from the HTML page
def get_metadata(htmlPage):
    # Python list to hold metadata
    info=[]

    # Opening and closing HTML title tags (these will be matched to find the header)
    openTag="<title>"
    closedTag="</title>"
    
    # If the title tag was not found append n/a to the list
    if openTag not in htmlPage or closedTag not in htmlPage:
        info.append("N/A")
    else:
        # Title header
        # Find the index of the starting and ending tag
        index=htmlPage.find(openTag)
        start=index+len(openTag)
        end=htmlPage.find(closedTag)

        # Get the substring from the start of end of the opening title tag till the end of the closing title tag
        info.append(htmlPage[start:end])
    
    # Split the text on "datePublished"
    tempSplitPub=htmlPage.split("datePublished\":\"")
    
    # Check if dataPublished was found
    if len(tempSplitPub)>1:
        # Publishing date header
        tempPub=tempSplitPub[1]
        info.append(tempPub[:10])
    else:
        # If not found append n/a to the list
        info.append("N/A")
    
    # Split the text on "dateModified"
    tempSplitMod=htmlPage.split("dateModified\":\"")
    
    # Check if dateModified was found
    if len(tempSplitMod)>1:
        # Get the date most recently modified
        tempMod=tempSplitMod[1]
        info.append(tempMod[:10])
    else:
        # If not found append n/a to the list
        info.append("N/A")

    #Find the date of the document | split on "header_year_text"
    tempTextDate = htmlPage.split("<span id=\"header_year_text\">")
    
    # Check if document date was found
    if len(tempTextDate) > 1: 
        # Extract document date from the string
        tempText = tempTextDate[1]
        tempText = re.sub("</span>[\S\s]*", "", tempText)
        tempText = re.sub("&.*;\(", "", tempText)
        tempText = re.sub("\)[\S\s]*", "", tempText)
        # Append the date to the list
        info.append(tempText)
    else:
        # If not found append n/a to the list
        info.append("N/A")

    # Return metadata
    return info

#Take a url and return the HTML page
def find_html(purl):
    # Check if the page exists, if not return none
    try:
        status_code=urllib.request.urlopen(purl).getcode()
    except urllib.error.HTTPError as err:
        return None 
    
    # Otherwise, get the HTML from the page
    page=urlopen(purl)
    html_bytes=page.read()
    html = html_bytes.decode("utf-8")
    return html

#Get plain text from the HTML page, remove all tags
def get_text(html):
        page_text = ''
        soup = BeautifulSoup(html, 'lxml')
        #for script_tag in soup(["script", "style"]):
        #    script_tag.decompose()
        text = soup.find_all(text=True)
        for t in text:
            if t.parent.name not in inlist:
                page_text += t
        return page_text

#Open a new file for write only
def open_file(file_name):
    f = open(file_name, "w")
    return f

#Remove empty lines from the output string
def remove_empty(input_lines):
    lines = input_lines.split('\n')
    non_empty = [line for line in lines if line.strip() != '']

    returned_string = ''
    for line in non_empty:
        returned_string += line + '\n'

    return returned_string

# Compile data in pandas dataframe
def get_dataframe(metadata, text):
    # Create a dataframe to hold the metadata
    data = pd.DataFrame()

    # Loop through the page metadata, appending to the dataframe if available
    data = data.append({"Title" : metadata[0],
            "Date Published" : metadata[1],
            "Date Modified" : metadata[2],
            "Document Date" : metadata[3],
            "Text" : text},
            ignore_index=True)
    
    # Return the dataframe
    return data 

#Read the content of the page and print to a file
def readWebpage(pageCount):
    # ===============================================================================================================
    # GET DATABASE, MUST BE DONE INSIDE EACH THREAD | MONGODB CLIENT CANNOT BE CONVERTED INTO THREADED/LOCKED OBJECT
    # ===============================================================================================================
     
    # Get a connection to the server
    client = get_client()
    
    # Get a database from the connection
    database = get_database(client)

    # Get a collection from the database (WikiSourceText, holds the wikisource pages)
    collection = database.WikiSourceText

    # Loop through all the pages passed from the main, this is done on each thread 
    for i in range(pageCount):
        pageHtml=find_html(URL)

        # Flag to hold the value used to check for a page's existance
        flag = True

        # Write thread id, loop iteration, and page url to the console if found
        if pageHtml != None:
            print("Thread: " + str(mp.current_process()) + " Loop: " + str(i) + " | Page: " + URL)
        else:
            print("Thread: " + str(mp.current_process()) + " Loop: " + str(i) + " | Page: Error, Page Not Found") 
            flag = False
        
        # Check if page was found
        # We only want to write to the database if we found a page, thus this code will only be run if there is context on the HTML page.
        if flag == True:
            #Get the text from the HTML page, remove empty lines, and count the frequency of each word
            text = get_text(pageHtml)
            text = remove_empty(text)
            
            #Get metadata from the HTML file
            metadata=get_metadata(pageHtml)
	    
	    # Get the page data (text) and metadata
            page_dataframe = get_dataframe(metadata, text)

	    # Conver the dataframe to a dictionary to allow it to be written to the database
            page_dict = convert_to_dict(page_dataframe)
	
            # Add dictionary to the collection
            collection.insert_one(page_dict)

            # Set flag back to true 
            flag = True
    
    # Close the connection to the database         
    close_database(client) 

if __name__ =="__main__":
    # Create the multithreading pool
    pool=mp.Pool(mp.cpu_count())
    
    #Write the pages to the list
    pageCounts=[]
    for i in range(mp.cpu_count()):
        pageCounts.append(20)
    
    #Print information to the console to inform the user on the number of threads available
    print("Number of available processors: ", mp.cpu_count())

    #Start threads
    pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    
    #Stop threads and write output to console
    pool.close()
    print("Done... pulled files written to MongoDB database")
