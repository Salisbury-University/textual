import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import functools as ft
import multiprocessing as mp
url="https://en.wikipedia.org/wiki/Special:Random"

def find_info(htmlPage, tag):
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

def find_html(purl):
    page=urlopen(purl)
    html_bytes=page.read()
    html = html_bytes.decode("utf-8")
    return html
    


def readWebpage(pageCount):
    c=0
    for i in range(pageCount):
        c+=1
        pageHtml=find_html(url)
        print(find_info(pageHtml, "title"))
        print(find_info(pageHtml, "datepub"))
        print(find_info(pageHtml, "datemod"))
        print("Num loop: "+str(i))

if __name__ =="__main__":
    pool = mp.Pool(mp.cpu_count())
    pageCounts=[]
    for i in range(mp.cpu_count()):
        pageCounts.append(50)
    print("running")
    print("Number of available processors: ", mp.cpu_count())
    pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    pool.close()
    print(results)
