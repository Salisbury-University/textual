import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools as ft
import multiprocessing as mp
import threading
from collections import Counter
import time

#All punctuation characters
from string import punctuation

#Constant to 
URL="https://en.wikipedia.org/wiki/Special:Random"

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
    info=[]
    openTag="<title>"
    closedTag="</title>"
    if htmlPage is None:
        return info
    if openTag not in htmlPage or closedTag not in htmlPage:
        info.append("title not found")
    else:
        index=htmlPage.find(openTag)
        start=index+len(openTag)
        end=htmlPage.find(closedTag)
        info.append(htmlPage[start:end])
    tempSplitPub=htmlPage.split("datePublished\":\"")
    if len(tempSplitPub)>1:
        tempPub=tempSplitPub[1]
        info.append(tempPub[:10])
    tempSplitMod=htmlPage.split("dateModified\":\"")
    if len(tempSplitMod)>1:
        tempMod=tempSplitMod[1]
        info.append(tempMod[:10])
    return info

def find_info(htmlPage, tag):  # not being used now
    if htmlPage is None:
        return "web page not found"
    if "date" not in tag:
        openTag="<"+tag+">"
        closedTag="</"+tag+">"
        if openTag not in htmlPage or closedTag not in htmlPage:
            return "TAG NOT FOUND"
        index=htmlPage.find(openTag)
        start=index+len(openTag)
        end=htmlPage.find(closedTag)
        return htmlPage[start:end]
    elif tag=="datepub":
        tempSplit=htmlPage.split("datePublished\":\"")
        if len(tempSplit)>1:
            tempStr=tempSplit[1]
            return tempStr[:10]
        return "Date published not found"
    elif tag=="datemod":
        tempSplit=htmlPage.split("dateModified\":\"")
        if len(tempSplit)>1:
            tempStr=tempSplit[1]
            return tempStr[:10]
        return "Date most recently modified not found."

#Take a url and return the HTML page
def find_html(purl):
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

#Read the content of the page and print to a file
def readWebpage(pageCount):
		
		plaintext_file = open_file("plaintext.txt") 

		c=0
		flag=0
		try:
				status_code=urllib.request.urlopen(URL).getcode()
		except urllib.error.HTTPError as err:
				#print("http",err.code, "ERROR")
				flag=1
		if flag==0: 
				for i in range(pageCount):
						c+=1
						pageHtml=find_html(URL)
            #Get the text from the HTML page, remove empty lines, and count the frequency of each word
						text = get_text(pageHtml)
						text = remove_empty(text)
            
            #Get metadata from the HTML file
						metadata=get_metadata(pageHtml)

            #Save page source to a separate file
						save_html(pageHtml, metadata[0])

            #Print the page metadata to the screen
						#for data in metadata:
								#print(data)

            #Ensure thread synchronization to avoid race condition
						while global_lock.locked():
								time.sleep(0.01)

            #If the lock is available, grab it write the metadata and frequency to the file and return the lock
						global_lock.acquire()

						plaintext_file.write(metadata[0])
						plaintext_file.write("\n")
						plaintext_file.write(text)
						plaintext_file.write("\n=========\n")

						for data in metadata:
								output_file.write(data + '\n')
						output_file.write('\n')
						freq_list = freq_count(text)
           
            #Print the frequency for each word
						output_file.write(freq_list + '\n')
        
						global_lock.release()
						#print("Num loop: "+str(i)) 
		flag=0


if __name__ == "__main__":
    #Open the output file
    output_file = open_file("output.txt")
    pool=mp.Pool(mp.cpu_count()//4)
    
    #Write the pages to the list
    pageCounts=[]
    for i in range(mp.cpu_count()//4):
        pageCounts.append(25)
    
    #Print information to the console to inform the user
    #print("running")
    #print("Number of available processors: ", mp.cpu_count())

    #Start threads
    pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    
    #Stop threads and write output to console
    pool.close()
    #print("Done... output saved to file")

    #Close output file
    output_file.close()
