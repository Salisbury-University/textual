import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import functools as ft
import multiprocessing as mp
import threading
from collections import Counter
from string import punctuation
numIter=10
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
        if end-start<100:
            return htmlPage[start:end]
        else:
            return htmlPage[start:start+150]


def get_date(html_page):
    openT="Release Date:"
    closedT="Language: "
    if html_page is None:
        return "DATE NOT FOUND"
    elif openT not in html_page or closedT not in html_page:
        return"Date not found on page"
    else:
        index=html_page.find(openT)
        start=index+len(openT)
        end=html_page.find(closedT)
        return html_page[start:end]


def get_author(html_page):
    openT="Author:"
    closedT="Posting Date:"
    closedT2="Release Date:"
    if html_page is None:
        return "AUTHOR NOT FOUND"
    elif openT not in html_page:
        return "Author not found in page"
    else:
        index=html_page.find(openT)
        start=index+len(openT)
        end=html_page.find(closedT)
        end2=html_page.find(closedT2)
        if closedT not in html_page and closedT2 not in html_page:
            print("not in at all")
        elif len(html_page[start:end])<len(html_page[start:end2]):
            return html_page[start:end]
        else:
            return html_page[start:end2]


def readWebpage(pageCount):
    print(pageCount)
    totalLen=0
    for i in range(numIter):
        '''if (i%(numIter//10)==0 and i!=0):
            tempPName=str(mp.current_process())
            tempPSplit=tempPName.split("ForkPoolWorker-")
            tempPSplit2=tempPSplit[1].split("\' parent=")
            print(str(i)+" iterations for processor: "+str(tempPSplit2[0])+" ========================================================================")
        '''
        num=pageCount+i
        flag=0
        tempURL=URLBEGIN+"/"+str(num)+"/pg"+str(num)+".txt"
        url_str=tempURL
        try:
            status_code=urllib.request.urlopen(url_str).getcode()
        except urllib.error.HTTPError as err:
            #print("http",err.code, "ERROR")
            flag=1
        if flag==0:
            pageHtml=find_html(tempURL)
            totalLen+=(len(pageHtml))
            if "Language: English" not in pageHtml:
                print("Warning: Source may not be in English")
            #print(totalLen)
            print(tempURL)
            title=get_title(pageHtml)
            if len(title)<1000:
                print(title)
            else:
                print("Title too long")
            date=get_date(pageHtml)
            print(date)
            author=get_author(pageHtml)
            print(author)
        flag=0
    return totalLen

if __name__=="__main__":
    pool=mp.Pool(mp.cpu_count())
    count=0
    pageCounts=[]
    for i in range(mp.cpu_count()):
        pageCounts.append(count*numIter+1)
        count+=1
    results=pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    print(results)
    totalLen=0
    for i in results:
        totalLen+=i
    pool.close()
    print("Average HTML length= "+str(round(totalLen/(numIter*mp.cpu_count()),2)))
    print("Done")
