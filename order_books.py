import requests
import json
from pandas import DataFrame

URL = 'https://coincheck.com/api/order_books'
coincheck = requests.get(URL).json() 
for key in coincheck.keys():
    print(key, ":")
    for value in coincheck[key]:
        print(value)
    print("--------------------------------------")
