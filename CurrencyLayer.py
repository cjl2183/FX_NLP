import datetime
import pandas as pd
import numpy as np
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

loc = os.getcwd()
sys.path.append(os.path.abspath('nytimesarticle-0.1.0'))

from get_NYT import get_NYT
ACCESS_KEY='18397b8a5f249028c58514c15cfa93fa'

from get_fx import get_fx
url = 'http://apilayer.net/api/historical?'


if __name__ == '__main__':

	today = datetime.date.today()
	end = str(today.year)+str(today.month).zfill(2)+str(today.day).zfill(2)
	brexit_dt = datetime.date(2016,6,23)
	start = str(brexit_dt.year)+str(brexit_dt.month).zfill(2)+str(brexit_dt.day).zfill(2)
	hist = today - brexit_dt

	'''
	Get NYTimes articles
	THIS ONLY RETURNS 10 ARTICLES IN ONE QUERY. NEED TO FIX.
	'''
	dates, corpus = get_NYT(start, end)

	'''
	Get historical FX rates

	#fx_prices = get_fx(ACCESS_KEY, url, brexit_dt, today)
	fx_prices = pd.read_csv('GBPUSD.csv',header=None)
	'''

	'''
	Calculate 1-day price change directions

	df_move = np.array(fx_prices.iloc[:-1,1]) - np.array(fx_prices.iloc[1:,1])
	#print df_move
	df_signal = np.sign(df_move)
	#rng = pd.date_range(end=end, periods=hist.days+1, freq='D')
	df_chg = pd.Series(df_signal,index=fx_prices.iloc[1:,0])
	df_chg.to_csv('GBPUSD_CHNG.csv')
	'''
	df_chg = pd.read_csv('GBPUSD_CHNG.csv',header=None,names=['date','change'])
	df_chg = df_chg.set_index(pd.DatetimeIndex(df_chg['date']))
	#df_chg.set_index('date',inplace=True)
	#df_chg.set_index(pd.to_datetime(df_chg['date']),inplace=True)

	count_vec = CountVectorizer(min_df=1,stop_words='english',lowercase=True)
	tfidf_vec = TfidfVectorizer(sublinear_tf=True, max_df=0.5,stop_words='english',lowercase=True)
	datetimes = [pd.to_datetime(dt) for dt in dates]
	max_dt = max(datetimes)
	curr_articles = sum(np.array(datetimes) == max_dt)
	print "number of articles today: {}".format(curr_articles)
	X = count_vec.fit_transform(corpus)

	'''
	Lookup price changes for article dates
	'''
	Y = []
	for dt in dates:
		Y.append(df_chg.loc[dt]['change'])
	df_px_article = pd.DataFrame(Y,index=pd.DatetimeIndex(dates),columns=['PriceChg'])
	print df_px_article
	#print Y


	'''
	Fit and predict Naive Bayes
	'''
	clf = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
	remove = sum(curr_articles)
	clf.fit(X[:-remove,:], Y[:-remove])
	print clf.predict(X[-remove])
	#print clf.score(X,Y)
	#print clf.class_count_
