import nytimesarticle
import pandas as pd

def get_NYT(start, end):
	NYT_ARTICLE = 'deffb8ca21824660b6e431b160550918'
	NYT_SEMANTIC = 'deffb8ca21824660b6e431b160550918'
	#api = nytimesarticle.search()
	api = nytimesarticle.articleAPI(NYT_ARTICLE)

	articles = api.search( q = 'brexit', fq = {'source':['Reuters','AP', 'The New York Times'],\
		'news_desk':["Foreign","Business","Financial","Market Place","World"],'document_type':"article"}, begin_date = start, 
		end_date = end, sort= "newest", \
	 	fl = "web_url,snippet,lead_paragraph,abstract,source,headline,keywords,pub_date,document_type,news_desk,type_of_material", \
	 	facet_field = "source,section_name,document_type")
	dates = []
	corpus = []
	print len(articles['response']['docs'])
	for doc in articles['response']['docs']:
		#print doc['web_url']
		dates.append(pd.to_datetime(doc['pub_date'][0:10]))
		corpus.append(doc['lead_paragraph'])
	return dates,corpus

if __name__ == '__main__':
	get_fx(sys.argv[1],sys.argv[2],sys.argv[3])