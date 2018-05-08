


def cnbc_results(bsObj):    #needs a beautifulSoup object inputted
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
            video=True
            print "cnbc video link"
            sentiment="Video"
            data.append({'link':link, 'headline': headline, 'postDate':postDate, 'sentiment':sentiment, 'article':'video'})
            continue
        article_soup=bsoup(article_html,'html.parser')
        article_soup.find(attrs={'class':re.compile(r".*\bstory\b.*")})
        article_text=article_soup.get_text()
        clean_article_text=clean_article(article_text)
        article_in_array=[clean_article_text]
        sentiment=sentiment_analysis(article_in_array)
        data.append({'link':link, 'headline': headline, 'postDate':postDate, 'sentiment':sentiment, 'article':article_text})
    return data
