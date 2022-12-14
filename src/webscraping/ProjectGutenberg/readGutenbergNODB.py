import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools as ft
import multiprocessing as mp
import threading
from collections import Counter
from string import punctuation

#Holds the number of iterations that each processor will run
numIter=20

#Beginning of the URL that will be used to make the url of different sources
URLBEGIN="https://www.gutenberg.org/cache/epub"

def find_html(purl):
    '''Gets the html from the provided site'''    
    page=urlopen(purl)
    html_bytes=page.read()
    html=html_bytes.decode("utf-8")
    #decodes the html bytes into readable html code
    return html

def get_title(htmlPage):
    '''Gets the title of the provided site'''
    openT="Title:"
    #Gutenberg saves the titles of the webpage between the title tag and the author tag
    closedT="Author:"
    if htmlPage is None: #Runs if the html page is empty
        return "TITLE NOT FOUND"
    else: #Runs if the html page is not empty
        index=htmlPage.find(openT)
        start=index+len(openT)
        end=htmlPage.find(closedT)
        if end-start<100:#Returns the title if the title is not too long
            return htmlPage[start:end]
        else:#Returns the first 150 characters if the title is too long
            return htmlPage[start:start+150]


def get_date(html_page):
    '''Gets the release date of the source'''
    openT="Release Date:"
    closedT="\n"
    if html_page is None: #Runs if the html page is empty
        return "DATE NOT FOUND"
    elif openT not in html_page or closedT not in html_page: #Runs if the tags for the data are not found in the page
        return"Date not found on page"
    else:
        index=html_page.find(openT)
        start=index+len(openT)
        end=html_page.find(closedT, start)
        return html_page[start:end] #Returns the date of the source is one is found


def get_author(html_page):
    '''Gets the author of the source'''
    openT="Author:"
    closedT="Posting Date:"
    closedT2="Release Date:"
    if html_page is None: #Runs if the html page is empty
        return "AUTHOR NOT FOUND"
    elif openT not in html_page: #Runs if the author tag is not found
        return "Author not found in page"
    else:#Returns the author line if the author tag is found in the page
        index=html_page.find(openT)
        start=index+len(openT)
        end=html_page.find(closedT)
        end2=html_page.find(closedT2)
        end3=html_page.find("\n", start)
        return html_page[start:end3]


def readWebpage(pageCount):
    '''Creates the URL to search and collects the metadata'''
    print(pageCount)
    totalLen=0
    for i in range(numIter): #Runs the specified number of times
        num=pageCount+i
        flag=0
        tempURL=URLBEGIN+"/"+str(num)+"/pg"+str(num)+".txt" #Creates the link for the page that will be searched
        url_str=tempURL
        try:
            status_code=urllib.request.urlopen(url_str).getcode() #Makes sure that the page exists
        except urllib.error.HTTPError as err:#Runs if the page does not exist
            flag=1
        if flag==0: #Only runs if the page exists
            pageHtml=find_html(tempURL)
            totalLen+=(len(pageHtml))
            if "Language: English" not in pageHtml: #ProjectGutenberg sometimes has a language tag
                print("Warning: Source may not be in English")
            print(tempURL)
            title=get_title(pageHtml) #Gets the title of the webpage
            if len(title)<1000:
                print(title)
            else:
                print("Title too long")
            date=get_date(pageHtml) #Gets the source's publishing date
            print(date)
            author=get_author(pageHtml) #Gets the source's author
            print(author)
        flag=0
    return totalLen

if __name__=="__main__":
    #Creates the pool of processors to be used
    pool=mp.Pool(mp.cpu_count())
    count=0
    pageCounts=[]
    for i in range(mp.cpu_count()): #Creates the starting point for each of the processors
        pageCounts.append(count*numIter+1)
        count+=1
    results=pool.map(readWebpage, [pageNum for pageNum in pageCounts]) #Runs readWebpage on all processors
    print(results)
    totalLen=0
    for i in results:
        totalLen+=i
    pool.close()
    print("Average HTML length= "+str(round(totalLen/(numIter*mp.cpu_count()),2))) #Calculates the average html length for all sources
    print("Done")
