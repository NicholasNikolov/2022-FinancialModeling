# import requests
#
# headers = {
#   "apikey": "2d3e1b70-8887-11ec-9541-fdb5a8979f9d"}
#
# params = (
#    ("keyword[]", "AAPL"),
#    ("hl","en"),
# );
#
# response = requests.get('https://app.zenserp.com/api/v1/trends', headers=headers, params=params);


from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["AAPL"]  # list of keywords to get data

pytrends.build_payload(kw_list, cat=0, timeframe='now 1-d')

# 1 Interest over Time
data = pytrends.interest_over_time()
data = data.reset_index()
