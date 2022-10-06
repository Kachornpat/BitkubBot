from bitkubchecker import Bitkub
import time

def SMA(data, n):

    sum = 0
    data = data[:n]

    for i in data:
        sum = sum + i

    avg = sum/len(data)
    return avg


def EMA(CURR_P, PREV_EMA, K):
    return (CURR_P * K) + (PREV_EMA * (1 - K))



symbol = 'BTC_THB'

n1 = 10
n2 = 50

smoothing = 2

K1 = smoothing/(n1 + 1)    
K2 = smoothing/(n2 + 1)

EMA_N1 = []
x1 = []
EMA_N2 = []
x2 = []

data = []


Bitkub = Bitkub()

for i in range(0, n2):
    curr_last = Bitkub.Ticker('THB_BTC')['last']
    data.append(curr_last)
    print(curr_last)
    time.sleep(60)
    
print("Collecting data finished")

EMA_N1_1 = SMA(data, n1)
EMA_N2_1 = SMA(data, n2)


PREV_EMA_N1 = EMA_N1_1


for i in range(n1, n2):
    CURR_EMA_N1 = EMA(data[i], PREV_EMA_N1, K1)
    PREV_EMA_N1 = CURR_EMA_N1

PREV_EMA_N2 = EMA_N2_1


trend = ""

threshold = 100

while True:
    new_data = Bitkub.Ticker('THB_BTC')

    CURR_EMA_N1 = EMA(new_data['last'], PREV_EMA_N1, K1)
    PREV_EMA_N1 = CURR_EMA_N1

    CURR_EMA_N2 = EMA(new_data['last'], PREV_EMA_N2, K2)
    PREV_EMA_N2 = CURR_EMA_N2

    if trend == "" and CURR_EMA_N1 - CURR_EMA_N2 > threshold:
        trend = "Bullish"
    elif  trend == "" and  CURR_EMA_N2 - CURR_EMA_N1 > threshold:
        trend = "Bearish"

    if trend == "Bullish" and CURR_EMA_N2 - CURR_EMA_N1 > threshold:
        trend = "Bearish"
        print("Sell ", new_data['highestBid'])
    if trend == "Bearish" and CURR_EMA_N1 - CURR_EMA_N2 > threshold:
        trend = "Bullish"
        print("Buy ", new_data['lowestAsk'])

    print(CURR_EMA_N1," ", CURR_EMA_N2, " ", trend)
        
    time.sleep(60)

    
