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
        if end-start<100:
            return htmlPage[start:end]
        else:
            return htmlPage[start:start+150]


def get_date(html_page):
    openT="Release Date:"
    if html_page is None:
        return "DATE NOT FOUND"
    elif openT not in html_page:
        return"Copyright not found in page"
    else:
        index=html_page.find(openT)
        start=index+len(openT)
        end=start+20
        return html_page[start:end]


def readWebpage(pageCount):
    print(pageCount)
    totalLen=0
    for i in range(numIter):
        if (i%(numIter//10)==0 and i!=0):
            tempPName=str(mp.current_process())
            tempPSplit=tempPName.split("ForkPoolWorker-")
            tempPSplit2=tempPSplit[1].split("\' parent=")
            print(str(i)+" iterations for processor: "+str(tempPSplit2[0])+" ========================================================================")
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
            #print(totalLen)
            print(tempURL)
            title=get_title(pageHtml)
            if len(title)<1000:
                print(title)
            else:
                print("Title too long")
            date=get_date(pageHtml)
            print(date)
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
