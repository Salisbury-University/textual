import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import functools as ft


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
        tempStr=tempSplit[1]
        return tempStr[:10]
    elif tag=="datemod":
        tempSplit=htmlPage.split("dateModified\":\"")
        tempStr=tempSplit[1]
        return tempStr[:10]

def read_webpage(purl):
    page=urlopen(purl)
    html_bytes=page.read()
    html = html_bytes.decode("utf-8")
    return html
    


if __name__=="__main__":
    for i in range(100):
        url="https://en.wikipedia.org/wiki/Special:Random"
        page=urlopen(url)
        htmlBytes=page.read()
        pageHtml=htmlBytes.decode("utf-8")
        print(find_info(pageHtml, "title"))
        print(find_info(pageHtml, "datepub"))
        print(find_info(pageHtml, "datemod"))
