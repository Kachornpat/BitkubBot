from bitkubchecker import Bitkub
from pprint import pprint 
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time


symbol = 'BTC_THB'


Bitkub = Bitkub()
# pprint(Bitkub.Ticker('THB_BTC'))

def datetimeToSecond(day=0, hour=0, mins=0, sec=0):
    time_in_sec = (day * 86400) + (hour * 3600) + (mins * 60) + sec
    return time_in_sec
    

current_time = int(Bitkub.ServerTime())
from_time = current_time - datetimeToSecond(day=3)

print('from ', datetime.fromtimestamp(from_time).strftime("%A, %B %d, %Y %I:%M:%S"))
print('to ', datetime.fromtimestamp(current_time).strftime("%A, %B %d, %Y %I:%M:%S"))

dict_list = Bitkub.TradingView(symbol,'5', from_time, current_time)

def SMA(data, n):

    sum = 0
    data = data['c'][:n]

    for i in data:
        sum = sum + i

    avg = sum/len(data)
    return n, avg


def EMA(CURR_P, PREV_EMA, K):
    return (CURR_P * K) + (CURR_P * (1 - K))
        



n1 = 25
n2 = 50

smoothing = 2

K1 = smoothing/(n1 + 1)    
K2 = smoothing/(n1 + 1)

EMA_1_N1 = SMA(dict_list, n1)

PREV_EMA_N1 = EMA_1_N1[1]

for value in dict_list['c'][n1:n2]:
    EMA_1_N2_N1 = EMA(value, PREV_EMA_N1, K1)
    PREV_EMA_N1 = EMA_1_N2_N1
    

EMA_1_N2 = SMA(dict_list, n2)

x = []
y = []    

x2 = []
y2 = []

x.append(50)
y.append(EMA_1_N2_N1)
x2.append(EMA_1_N2[0])
y2.append(EMA_1_N2[1])



plt.scatter(x, y)
plt.scatter(x2, y2)
# plt.plot(x, y, linestyle = 'dotted')
# plt.plot(x2, y2, color = 'orange')
# plt.plot(x3, y3, color = 'r')
plt.show()

# current_time = int(Bitkub.ServerTime())
# prev_time = current_time
# while True:
#     current_time = int(Bitkub.ServerTime())
#     dict_list = Bitkub.TradingView(symbol,'1', prev_time, current_time)
#     print(dict_list)
#     time.sleep(60)
