import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools as ft
import multiprocessing as mp
import threading
from collections import Counter
from string import punctuation
numIter=100
URLBEGIN="https://www.gutenberg.org/cache/epub"

def find_html(purl):
    page=urlopen(purl)
    html_bytes=page.read()
    html=html_bytes.decode("utf-8")
    return html

def get_title(htmlPage):
    openT="Title:"
    closedT="Author:"
    if htmlPage is None:
        return "TITLE NOT FOUND"
    else:
        index=htmlPage.find(openT)
        start=index+len(openT)
        end=htmlPage.find(closedT)
        return htmlPage[start:end]


def get_date(html_page):
    openT="Copyright, "
    if html_page is None or openT not in html_page:
        return "DATE NOT FOUND"
    else:
        index=html_Page.find(openT)
        start=index+len(openT)
        end=start+4
        return htmlPage[start:end]


def readWebpage(pageCount):
    print(pageCount)
    for i in range(numIter):
        num=pageCount+i
        flag=0
        tempURL=URLBEGIN+"/"+str(num)+"/pg"+str(num)+".txt"
        print(tempURL)
        url_str=tempURL
        try:
            status_code=urllib.request.urlopen(url_str).getcode()
        except urllib.error.HTTPError as err:
            print("http",err.code, "ERROR")
            flag=1
        if flag==0:
            pageHtml=find_html(tempURL)
            title=get_title(pageHtml)
            if len(title)<1000:
                print(title)
            date=get_date(pageHtml)
            print(date)
        flag=0
    return 0

if __name__=="__main__":
    pool=mp.Pool(mp.cpu_count())
    count=0
    pageCounts=[]
    for i in range(mp.cpu_count()):
        pageCounts.append(count*numIter+1)
        count+=1
    results=pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    pool.close()
    print("Done")
