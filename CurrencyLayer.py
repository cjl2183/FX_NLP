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
'''
#Put into a nice, clean JSON in the gitignore directory
'''
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

	'''Load price change file
	'''
	df_chg = pd.read_csv('GBPUSD_CHNG.csv',header=None,names=['date','change'])
	df_chg = df_chg.set_index(pd.DatetimeIndex(df_chg['date']))

	'''Grab new FX prices and calculate changes
	'''
	max_dt = max(pd.to_datetime(df_chg['date']))
	start_dt = max_dt.date() + datetime.timedelta(1)
	if max_dt.date() <> today:
		fx_price_gap = get_fx(ACCESS_KEY, url, start_dt, today)
		dt_index = pd.date_range(start_dt,periods=(today-start_dt).days+1,freq='D')[::-1]
		#pd_fx_prices = pd.Series(fx_prices_more,index=dt_index)
		#fx_prices_more = pd.DataFrame(fx_prices_gap,columns=['price'], index=dt_gap)
		dt_gap = [str(d.date()) for d in dt_index]
		dt_gap = pd.DataFrame(dt_gap)
		fx_prices_more = pd.DataFrame(fx_price_gap)
		fx_px_delta = pd.concat([dt_gap,fx_prices_more], axis=1)
		fx_px_delta.columns = ['date','price']
		#print fx_px_delta
		fx_price_hist = pd.read_csv('GBPUSD.csv',names=['date','price'],header=0)
		#print fx_price_hist
		fx_prices = pd.concat([fx_px_delta,fx_price_hist],axis=0)
		#print fx_prices
		#fx_px_delta.append(fx_prices,ignore_index=True)
		fx_prices.to_csv('GBPUSD.csv',index=False)
		'''
		fx_px_delta.set_index(['date'],inplace=True)
		fx_prices_delta.index = pd.to_datetime(fx_prices_delta.index)
		print fx_prices
		fx_prices_total = fx_prices.append(pd_fx_prices)
		print fx_prices_total
		fx_prices_total.to_csv('GBPUSD.csv',header=True,index=True)
		'''
		'''Calculate 1-day price change directions
		'''
		df_move = np.array(fx_prices.iloc[:-1,1]) - np.array(fx_prices.iloc[1:,1])
		df_signal = np.sign(df_move)
		#rng = pd.date_range(end=end, periods=hist.days+1, freq='D')
		df_chg = pd.Series(df_signal,index=fx_prices.iloc[:-1,0])
		df_chg.to_csv('GBPUSD_CHNGv2.csv')


	#df_chg.set_index('date',inplace=True)
	#df_chg.set_index(pd.to_datetime(df_chg['date']),inplace=True)

	datetimes = [pd.to_datetime(dt) for dt in dates]
	max_dt = max(datetimes)
	curr_articles = sum(np.array(datetimes) == max_dt)
	print "number of articles today: {}".format(curr_articles)

	'''
	Lookup price changes for article dates
	'''
	Y = []
	for dt in dates:
		Y.append(df_chg.loc[dt.date()]['change'])
	df_px_article = pd.DataFrame(Y,index=pd.DatetimeIndex(dates),columns=['PriceChg'])
	print df_px_article

	'''
	Divide data into train vs. test groups
	'''
	count_vec = CountVectorizer(min_df=1,stop_words='english',lowercase=True)
	tfidf_vec = TfidfVectorizer(sublinear_tf=True, max_df=0.5,stop_words='english',lowercase=True)
	print corpus[:-curr_articles]
	print corpus[-curr_articles:]

	X_train = count_vec.fit_transform(corpus[:-curr_articles])
	X_test = count_vec.transform(corpus[-curr_articles:])
	Y_train, Y_test = Y[curr_articles:], Y[:curr_articles]
	#Y_train, Y_test = df_px_article.loc[Y_train]['PriceChg'], df_px_article.loc[Y_test]['PriceChg']

	'''
	Fit and predict Naive Bayes
	'''
	clf = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
	clf.fit(X_train, Y_train)
	print clf.predict(X_test)
	#print clf.score(X,Y)
	#print clf.class_count_