import pandas as pd
import numpy as np
import datetime
import requests
import json
import sys

def get_fx(ACCESS_KEY, url, start, end):
	prices = np.array([])
	mydict = {'access_key':ACCESS_KEY,'currencies':'GBP','format':'1'}
	hist = end - start
	rng = pd.date_range(end=end, periods=hist.days+1, freq='D')

	for i in xrange(hist.days+1):
		delta = datetime.timedelta(days=i)
		hist_dt = end-delta
		Y = hist_dt.year
		M = hist_dt.month
		D = hist_dt.day
		D_str = str(D).zfill(2)
		M_str = str(M).zfill(2)
		dt_str = str(Y)+'-'+M_str+'-'+D_str
		mydict['date']=dt_str
		resp = requests.get(url,params=mydict)
		parsed = json.loads(resp.text)
		rate = 1/float(parsed['quotes']['USDGBP'])
		prices = np.append(prices,rate)
	df_fx = pd.Series(prices,index=rng[::-1])
	df_fx.to_csv('GBPUSD_delt.csv')
	return prices

if __name__ == '__main__':
	get_fx(sys.argv[1],sys.argv[2],sys.argv[3])