# 3 OCT 2022
import requests
import json
import hmac
import hashlib

API_HOST = 'https://api.bitkub.com'

class Bitkub():

    __API_KEY = 'YOUR API KEY'
    __API_SECRET = b'YOUR API SECRET'
    
    def SetAPIkey(self, key, secret):
        self.__API_KEY = key
        self.__API_SECRET = secret

    def Ticker(self, symbol):
        try: 
            response = requests.get(API_HOST + "/api/market/ticker")
            return response.json()[symbol]
        except:
            return 'Error Occur'

    def TradingView(self, symbol, resolution, from_time, to_time):
        try:
            response = requests.get(API_HOST + f"/tradingview/history?symbol={symbol}&resolution={resolution}&from={from_time}&to={to_time}")
            return response.json()
        except:
            return None
    
    def ServerTime(self):
        try:
            response = requests.get(API_HOST + '/api/servertime')
            return response.text
        except:
            return None
    

    def GetBalance(self):
        # check server time
        response = requests.get(API_HOST + '/api/servertime')
        ts = int(response.text)
        print('Server time: ' + response.text)

        # check balances
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': self.__API_KEY,
        }
        data = {
            'ts': ts,
        }

        # json_encode()
        j = json.dumps(data, separators=(',', ':'), sort_keys=True)
        print('Signing payload: ' + j)

        # sign()
        h = hmac.new(self.__API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
        signature = h.hexdigest()
        data['sig'] = signature
        print('Payload with signature: ' + json.dumps(data, separators=(',', ':'), sort_keys=True))

        response = requests.post(API_HOST + '/api/market/balances', headers=header, data=json.dumps(data, separators=(',', ':'), sort_keys=True))

        print('Balances: ' + response.text)