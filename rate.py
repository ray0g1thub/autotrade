import requests
import json
from pandas import DataFrame

URL = 'https://coincheck.com/api/exchange/orders/rate'
params = {'order_type': 'sell', 'pair': 'btc_jpy', 'amount': 0.005}
coincheck = requests.get(URL, params=params).json() 
print(coincheck)

if (coincheck['success'] == True):
    print("price : " + coincheck['price'] )
    print("rate : " + coincheck['rate'] )
