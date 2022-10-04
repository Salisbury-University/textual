import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import functools as ft
import multiprocessing as mp
import threading
from collections import Counter
from string import punctuation
numIter=50
URLBEGIN="https://www.gutenberg.org/files/"

def find_html(purl):
    page=urlopen(purl)
    html_bytes=page.read()
    html=html_bytes.decode("utf-8")
    return html

def get_title(htmlPage):
    openT="<title>"
    closedT="</title>"
    if htmlPage is None:
        return "TITLE NOT FOUND"
    else:
        index=htmlPage.find(openT)
        start=index+len(openT)
        end=htmlPage.find(closedT)
        return htmlPage[start:end]


def readWebpage(pageCount):
    print(pageCount)
    for i in range(numIter):
        num=pageCount+i
        tempURL=URLBEGIN+str(num)+"/"+str(num)+"-h/"+str(num)+"-h.htm"
        print(tempURL)
        pageHtml=find_html(tempURL)
        title=get_title(pageHtml)
        if len(title)<1000:
            print(title)
    return 0

if __name__=="__main__":
    pool=mp.Pool(1)
    count=0
    pageCounts=[]
    for i in range(1):
        pageCounts.append(count*numIter+1)
        count+=1
    results=pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    pool.close()
    print("Done")
