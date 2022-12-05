import requests
import zlib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools as ft
import multiprocessing as mp
import threading
from collections import Counter
from string import punctuation
from pymongo import MongoClient

tagList=['[document]','noscript','header','html','meta','head', 'input', 'script', 'style', 'script', 'footer']

#Holds the number of iterations that each processor will run
numIter=100

#Beginning of the URL that will be used to make the url of different sources
URLBEGIN="https://www.gutenberg.org/cache/epub"

def get_credentials():
    with open("mongopassword.txt","r") as pass_file:
        lines=pass_file.read().splitlines()
    pass_file.close()
    return lines

def get_client():
    # Needs to be done this way, can't push credentials to github
    # Call the get pass function to open the file and extract the credentials
    lines = get_credentials()

    # Get the username from the file
    username = lines[0]

    # Get the password from the file
    password = lines[1]
    
    # Set up a new client to the database
    # Using database address and port number
    client = MongoClient("mongodb://10.251.12.108:30000", username=username, password=password)

    # Return the client
    return client

def remove_empty(text):
    lines=text.split('\n')
    nonEmpt=[line for line in lines if line.strip()!='']
    listS=[]
    for l in nonEmpt:
        listS.append(l)
        listS.append('\n')
    return ''.join(listS)

def makeID(url):
    return str(hash(url))

def get_database(client):
	return client.textual

def close_database(client):
	client.close()

def save_html(html, pageID):
    htmlFile="HTML_ProjectGutenberg_"+str(pageID)+".html"
    file=open_file(htmlFile)
    file.writelines(html)
    file.close()

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

def get_text(html_page):
    '''Gets the text from the html of the page'''
    soup=BeautifulSoup(html_page,'lxml')
    text=soup.find_all(text=True)
    for tag in tagList:
        text=text.replace(tag,"");
    return text

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

def pageDict(metadata,text):
    pDict={'URL':metadata[0], 'title': metadata[1],'date':metadata[2],'author':metadata[3], 'text':text,'id': makeID(metadata[0])}
    return pDict

def htmlDict(html, URL):
    hDict={'HTML': zlib.compress(html.encode()), 'ID': makeID(URL)}
    return hDict
def readWebpage(pageCount):
    client=get_client()
    database=get_database(client)
    '''Creates the URL to search and collects the metadata'''
    print(pageCount)
    page_collection=database.PGText
    html_collection=database.PGHTML
    totalLen=0
    for i in range(numIter): #Runs the specified number of times
        metadata=[]
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
            pageText=get_text(pageHtml)
            pageText=remove_empty(text)
            metadata.append(tempURL)
            if "Language: English" not in pageHtml: #ProjectGutenberg sometimes has a language tag
                print("Warning: Source may not be in English")
            print(tempURL)
            title=get_title(pageHtml) #Gets the title of the webpage
            if len(title)<1000:
                metadata.append(title)
            else:
                metadata.append("Title too long")
            date=get_date(pageHtml) #Gets the source's publishing date
            metadata.append(date)
            author=get_author(pageHtml) #Gets the source's author
            metadata.append(author)
            page_collection.insert_one(pageDict(metadata,text))
            html_collection.insert_one(htmlDict(pageHtml,metadata[0]))
        flag=0
    close_database(client)
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
