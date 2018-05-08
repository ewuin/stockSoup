from .sentiment_script_cnbc import clean_article
from .sentiment_script_cnbc import sentiment_analysis
import re
import datetime
import urllib2
from django.core.validators import URLValidator

from bs4 import BeautifulSoup as bsoup


def cnbc_crawler(bsObj):    #needs a beautifulSoup object inputted
    data = []
    for node in bsObj.findAll(attrs={'class':re.compile(r".*\bSearchResultCard\b.*")}):
        #print node
        link=node.find("a").get("href")
        headline=node.find("h3").get_text()
        dateEl=str(node.find("time"))
        timeStamp=re.search(r'(\d+)',dateEl).group(0)
        postDate=datetime.datetime.fromtimestamp(int(timeStamp)/1000).strftime('%Y-%m-%d %H:%M:%S')
        print link
        try:
            article_html=urllib2.urlopen(link)
        except:
            print "cnbc video link"
            sentiment=sentiment_analysis([headline])+" / Video"
            data.append({'link':link, 'headline': headline, 'postDate':postDate, 'sentiment':sentiment, 'article':'video'})
            continue
        article_soup=bsoup(article_html,'html.parser')
        article_soup.find(attrs={'class':re.compile(r".*\bstory\b.*")})
        article_el=article_soup.find_all("p")
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
