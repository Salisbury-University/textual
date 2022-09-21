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

def get_text(html):
        soup = BeautifulSoup(html, 'lxml')
        for script_tag in soup(["script", "style"]):
            script_tag.decompose()
        text = soup.get_text()
        return text

def open_file(file_name):
    f = open(file_name, "w")
    return f

def close_file(file_name):
    file_name.close()

def readWebpage(pageCount):
    c=0
    output_file = open_file("output.txt")
    for i in range(pageCount):
        c+=1
        pageHtml=find_html(url)
        text = get_text(pageHtml)
        text = text.split('\n')
        metadata=get_metadata(pageHtml)
        for data in metadata:
            print(data)
        output_file.writelines(text)
        # print(text) 
        print("Num loop: "+str(i))
    output_file.close()

if __name__ =="__main__":
    if mp.cpu_count()>=4:
        pool=mp.Pool(int(mp.cpu_count())//2)
    else:
        pool=mp.Pool(mp.cpu_count())
    pageCounts=[]
    for i in range(mp.cpu_count()//2):
        pageCounts.append(50)
    print("running")
    print("Number of available processors: ", mp.cpu_count())
    pool.map(readWebpage, [pageNum for pageNum in pageCounts])
    pool.close()
