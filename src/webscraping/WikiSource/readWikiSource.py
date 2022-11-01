# Date: 10/1/2022-10/31/2022
# Description: Collect pages from the WikiSource website using HTTP requests
# Saving format: Currently in a txt file, holds all words in a frequency array

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

#Lock to avoid race condition when writing to the output file
global_lock = threading.Lock()

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

#Count the frequency of each word in the document
def freq_count(input_text):
    word_list = input_text.split()

    #Remove leading and trailing punctuation
    word_list = [clean_string(word) for word in word_list]

    #Output string
    output_text = ''
   
    #Get the count for each word
    unique_words = set(word_list)
    for words in unique_words:
        output_text += 'Frequency of ' + words + ': ' + str(word_list.count(words)) + '\n'

    #Return the frequency
    return output_text

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
    
    c=0
    for i in range(pageCount):
        c+=1
        pageHtml=find_html(URL)

        # Flag to hold the value used to check for a page's existance
        flag = True

        # Write thread id, loop iteration, and page url to the console if found
        if pageHtml != None:
            print("Thread: " + str(mp.current_process()) + " Loop: " + str(i) + " | Page: " + URL)
        else:
            print("Thread: " + str(mp.current_process()) + " Loop: " + str(i) + " | Page: N/A") 
            flag = False
        
        # Check if page was found
        if flag == True:
            #Get the text from the HTML page, remove empty lines, and count the frequency of each word
            text = get_text(pageHtml)
            text = remove_empty(text)
            
            #Get metadata from the HTML file
            metadata=get_metadata(pageHtml)

            #Save page source to a separate file
            save_html(pageHtml, metadata[0])

            #Print the page metadata to the screen
            #for data in metadata:
            #    print(data)

            # print(get_dataframe(metadata, text))

            #Ensure thread synchronization to avoid race condition
            while global_lock.locked():
                time.sleep(0.01)

            #If the lock is available, grab it write the metadata and frequency to the file and return the lock
            global_lock.acquire()
            #for data in metadata:
            #    output_file.write(data + '\n')
            #output_file.write('\n')
            #freq_list = freq_count(text)
           
            #Print the frequency for each word
            #output_file.write(freq_list + '\n')
            global_lock.release()
            # print("Num loop: "+str(i))
            flag = False

if __name__ =="__main__":
    #Open the output file
    output_file = open_file("output.txt")
    pool=mp.Pool(mp.cpu_count())
    
    #Write the pages to the list
    pageCounts=[]
    for i in range(mp.cpu_count()):
        pageCounts.append(20)
    
    #Print information to the console to inform the user
    print("Running")
    print("Number of available processors: ", mp.cpu_count())

    #Start threads
    pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    
    #Stop threads and write output to console
    pool.close()
    print("Done... output saved to file")

    #Close output file
    output_file.close()
