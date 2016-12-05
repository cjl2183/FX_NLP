import sys, os
sys.path.append(os.path.join(os.getcwd(), "nytimesarticle-0.1.0"))
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
import nytimesarticle
import pandas as pd
import requests
import re
import datetime
import json

def get_NYT(start, end):
    NYT_ARTICLE = 'deffb8ca21824660b6e431b160550918'
    NYT_SEMANTIC = 'deffb8ca21824660b6e431b160550918'
    #api = nytimesarticle.search()
    api = nytimesarticle.articleAPI(NYT_ARTICLE)
    start_dt = pd.to_datetime(start).date()
    end_dt = pd.to_datetime(end).date()
    num_days = (end_dt - start_dt).days
    articles = []
    for i in xrange(num_days+1):
        dt = start_dt + datetime.timedelta(i)
        dt_start = str(dt.year)+str(dt.month).zfill(2)+str(dt.day).zfill(2)
        dt_end = str(dt.year)+str(dt.month).zfill(2)+str(dt.day+1).zfill(2)
        #print dt_start
        #print dt_end
        result = api.search(q = 'brexit', fq = {'source':['Reuters','AP', 'The New York Times'],\
                                                  'news_desk':["Foreign","Business","Financial","Market Place","World"],
                                                  'document_type':"article"}, begin_date = dt_start, end_date = dt_start, \
                              sort= "newest", \
                              fl = "web_url,snippet,lead_paragraph,abstract,source,headline,keywords,pub_date,document_type,news_desk,type_of_material", \
                              facet_field = "source,section_name,document_type")
        for r in result:
            if r == unicode('response'):
                for k in result[r].keys():
                    if k == unicode('docs'):
                        for doc in result[r][k]:
                            articles.append(doc)
        #print len(articles)
                            
    dates = []
    corpus = []
    print len(articles)
    for art in articles:
        r = requests.get(art[unicode('web_url')])
        #print r
        tree = html.fromstring(r.content)
        contents = tree.xpath('//p[@class="story-body-text story-content"]/text()')
        body = []
        for t in contents: 
            if t.strip <> '': body.append(re.sub(r'[^\w]', ' ', t))
        corpus.append(''.join(body))
        dates.append(art[unicode('pub_date')][0:10])
    return dates, corpus

if __name__ == '__main__':
	get_fx(sys.argv[1],sys.argv[2],sys.argv[3])