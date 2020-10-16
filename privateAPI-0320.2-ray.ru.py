import json
import requests
import time
import hmac
import hashlib
import ticker
import k203ma_pdta as k

#-------------------------definition of Coincheck------------------------
class Coincheck:
    def __init__(self, access_key, secret_key, url='https://coincheck.com'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.url = url

    def get(self, path, params=None):
        if params != None:
            params = json.dumps(params)
        else:
            params = ''
        nonce = str(int(time.time()))
        message = nonce + self.url + path + params

        signature = self.getSignature(message)

        return requests.get(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def post(self, path, params):
        params = json.dumps(params)
        nonce = str(int(time.time()))
        message = nonce + self.url + path + params

        signature = self.getSignature(message)

        return requests.post(
            self.url+path,
            data=params,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def delete(self, path):
        nonce = str(int(time.time()))
        message = nonce + self.url + path

        signature = self.getSignature(message)

        return requests.delete(
            self.url+path,
            headers=self.getHeader(self.access_key, nonce, signature)
        ).json()

    def getSignature(self, message):
        signature = hmac.new(
            bytes(self.secret_key.encode('ascii')),
            bytes(message.encode('ascii')),
            hashlib.sha256
        ).hexdigest()

        return signature

    def getHeader(self, access_key, nonce, signature):
        headers = {
            'ACCESS-KEY': access_key,
            'ACCESS-NONCE': nonce,
            'ACCESS-SIGNATURE': signature,
            'Content-Type': 'application/json'
        }

        return headers
#--------------------end definition of Coincheck--------------------
#--------------------functions code----------------------------------

def buy(coincheck,market_buy_amount):
    path_orders = '/api/exchange/orders'
    params = {
        "pair": "btc_jpy",
        "order_type": "market_buy",
        "market_buy_amount": market_buy_amount
    }
    result = coincheck.post(path_orders, params)

    localtime = time.asctime(time.localtime(time.time()))
    print("BUY:",localtime)
    return result

def sell(amount,coincheck):
    path_orders = '/api/exchange/orders'
    params = {
        "pair": "btc_jpy",
        "order_type": "market_sell",
        "amount": amount
    }
    result = coincheck.post(path_orders, params)

    localtime = time.asctime( time.localtime(time.time()))
    print("SELL:",localtime)
    return result

def orders_opens(coincheck):
    path_orders_opens = '/api/exchange/orders/opens'
    result = coincheck.get(path_orders_opens)
    localtime = time.asctime( time.localtime(time.time()))
    print("OPENS:",localtime)
    return result

def transactions(coincheck):
    path_orders_transactions = '/api/exchange/orders/transactions'
    result = coincheck.get(path_orders_transactions)
    ocaltime = time.asctime( time.localtime(time.time()))
    print("TRANSACTIONS:",localtime)
    return result

def order_cancel(id,coincheck):
    path_orders_cancel = '/api/exchange/orders/' + str(id)
    result = coincheck.delete(path_orders_cancel)
    localtime = time.asctime( time.localtime(time.time()))
    print("CANCEL:",localtime)
    return result

def orders_blance(coincheck):
    path_orders_blance = '/api/accounts/balance'
    result = coincheck.get(path_orders_blance)
    localtime = time.asctime( time.localtime(time.time()))
    print("BLANCE:",localtime)
    return result

#--------------------end functions code------------------------------
#--------------------main code---------------------------------------
#--------------------initialization start----------------------------
access_key = ''
secret_key = ''

coincheck = Coincheck(access_key, secret_key)

trend_two = 0#MOM的趨勢(目前減兩分鐘前)
trend_one =  0#MOM的趨勢(目前減一分鐘前)
big_trend_one = 0;
big_trend = 0;
file_name = 'btc.csv'#預設excel的檔名
signal_buy_or_sell = 'buy'

ticker.init_coin_data(file_name);#初始化btc.csv檔

for i in range(0,12):#先取得兩分鐘的資料
    if (i==0):
        ticker.update(file_name);#更新最新一筆的資料
    else:
        time.sleep(60);#等60sec
        ticker.update(file_name);
#-------------------end initialization-------------------------------

while(True):#主程式的迴圈
    time.sleep(60);#等60sec
    ticker.update(file_name);#更新最新一筆的資料
    trend_two,trend_one = k.do_MOM(file_name);#計算MOM的趨勢和現在資料的數據
    big_trend_one,big_trend = k.do_MACD(file_name)

    if(signal_buy_or_sell == 'buy'):#如果買的模式
        if (float(trend_one) > 0 and float(big_trend) > 0 and float(big_trend_one) > 0):#如果趨勢向上並現在數據是正的
            result = buy(coincheck)
            ticker.update(file_name);
            signal_buy_or_sell = 'sell'

            time.sleep(2)
            check_blance = orders_blance(coincheck)
            print("JPY:",float(check_blance.get('jpy')))
            print("BTC:",float(check_blance.get('btc')))

    elif (signal_buy_or_sell == 'sell'):#判斷式是否為賣的模式

        time.sleep(2)
        [last,bid,ask]=ticker.newest_coin_data();

        time.sleep(2)#間隔開讀取coincheck的網站的指令
        p = transactions(coincheck)#取得之前的交易紀錄

        p.get('transactions')#讀取之前的交易紀錄
        unicode_r = p['transactions'][0]['rate']#取得最近一筆的交易紀錄
        r = float(unicode_r)
        s = ((last-r)/r)

        time.sleep(2)
        check_blance = orders_blance(coincheck)
        amount = float(check_blance.get('btc'))
        time.sleep(2)

        if ( float(s)  >= 0.006 ):
            print("STOP-PROFIT(0.006)")
            result = sell(amount,coincheck)
            ticker.update(file_name);
            signal_buy_or_sell = 'buy'

        elif ( float(s) <= -0.003 ) :#損失太多(停損)
            print("STOP-LOSS(0.003)")
            result = sell(amount,coincheck)
            ticker.update(file_name);
            signal_buy_or_sell = 'buy'

        else:#不屬於停利和停損
            if (float(trend_one) < 0 or float(big_trend_one) < 0):#正常的賣出點
                print("STRATEGY OUT")
                result = sell(amount,coincheck)
                ticker.update(file_name);
                signal_buy_or_sell = 'buy'

        time.sleep(2)
        check_blance = orders_blance(coincheck)
        print("JPY:",float(check_blance.get('jpy')))
        print("BTC:",float(check_blance.get('btc')))

#---------------------end main code-----------------------------------
