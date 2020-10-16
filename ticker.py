import requests
import json
from pandas import DataFrame

import csv
import time

URL = 'https://coincheck.com/api/ticker'

def init_coin_data(file_name):
    data = [['Volume','Close','Timestamp','Bid','High','Low','Ask']]
    [data,w,f] = open_coin_data(data,file_name);
    close_coin_data(data,w,f);
    print("init_csv")

def open_coin_data(data,file_name):
    f = open(file_name,'wb')
    w = csv.writer(f)
    return [data,w,f]

def close_coin_data(data,w,f):
    w.writerows(data);
    #print(data)
    f.close();

def read_csv(file_name):
    f = open(file_name,'r')
    reader = csv.reader(f)
    
    data = []
    
    for row in reader:
        data = data + [row]
        
    f.close()
    return data
    
def coin_data(data):
    coincheck = requests.get(URL).json()
    data = data + [
        [
            coincheck.get('volume'),
            coincheck.get('last'),
            coincheck.get('timestamp'),
            coincheck.get('bid'),
            coincheck.get('high'),
            coincheck.get('low'),
            coincheck.get('ask')
            ]
        ]
    return data

def newest_coin_data():
    coincheck = requests.get(URL).json()
    return [coincheck.get('last'),
            coincheck.get('bid'),
            coincheck.get('ask')]

def update(file_name):
    data = read_csv(file_name);
    [data,w,f] = open_coin_data(data,file_name);

    data = coin_data(data);

    close_coin_data(data,w,f);
    localtime = time.asctime( time.localtime(time.time()))
    print("Update the data",localtime)
