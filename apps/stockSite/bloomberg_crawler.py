from .sentiment_script_BB import clean_article
from .sentiment_script_BB import sentiment_analysis
import re
import datetime
import urllib2
from django.core.validators import URLValidator

from bs4 import BeautifulSoup as bsoup


def bb_crawler(bsObj):    #needs a beautifulSoup object inputted
    data = []
    for node in bsObj.findAll(attrs={'class':re.compile(r"^search-result$")}):
        headlineEl=node.find("h1")
        headline=node.find("h1").get_text().strip()
        link=headlineEl.find("a").get("href")
        dateEl=str(node.find(attrs={'class':re.compile(r"\bpublished-at\b")}) )
        timeStamp=re.search(r"datetime=\"(.*?)\"",dateEl).group(1)
        postDate=timeStamp
        article_html=urllib2.urlopen(link)
        article_soup=bsoup(article_html,'html.parser')
        articleDiv=article_soup.find(attrs={'class':re.compile(r"^body-copy-v2$")})
        if articleDiv==None:
            print articleDiv
            print "BB audio video link"
            sentiment=sentiment_analysis([headline])+" / Media"
            data.append({'link':link, 'headline': headline, 'postDate':postDate, 'sentiment':sentiment, 'article':'audio/video'})
            continue

        article_el=articleDiv.find_all("p")
        article_list=[]
        paragraphs=unicode("")
        for p in article_el:
            paragraph=p.get_text()
            article_list.append(paragraph)
        article_text=u" ".join(string for string in article_list)
        #print article_text
        clean_article_text=clean_article(article_text)
        article_in_array=[clean_article_text]
        sentiment=sentiment_analysis(article_in_array)
        data.append({'link':link, 'headline': headline, 'postDate':postDate, 'sentiment':sentiment, 'article':article_text})
    return data
