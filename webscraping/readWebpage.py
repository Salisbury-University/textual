import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import functools as ft
import multiprocessing as mp
url="https://en.wikipedia.org/wiki/Special:Random"

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
        metadata=get_metadata(pageHtml)
        for data in metadata:
            print(data)
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
