import pandas_datareader.data as pdr
import datetime
from nifty_stock_list import *

nfty_50 = nifty()

for i in nifty_50:
    print(i)
    ticker = i
    ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today() - datetime.timedelta(960), datetime.date.today())
    print(ohlcv)


    def macd(DF, a, b, c):
        df = ohlcv.copy()
        df["MA_Fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
        df["MA_Slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
        df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
        df["Signal"] = df["MACD"].ewm(span=c, min_periods=c).mean()
        df.dropna(inplace=True)
        # print(df.iloc[ : ,[5,8,9]])
        macd.dff = df.iloc[:, [5, 8, 9]]
        # print(macd.dff)
        return DF


    def get_buy_signal():
        global sell_price
        global buy_price
        global profit

        sell_price = []
        buy_price = []
        profit = []

        macd(ohlcv, 12, 26, 9)
        dict1 = macd.dff

        try:
            for i in range(len(dict1)):
                Macd = dict1.iloc[i]['MACD']
                signal = dict1.iloc[i]['Signal']

                Macd1 = dict1.iloc[i + 1]['MACD']
                signal1 = dict1.iloc[i + 1]['Signal']

                if Macd < signal and Macd1 > signal1:
                    print("BUY")
                    print(dict1.iloc[i + 1])
                    buy_price.append(dict1.iat[(i + 1), 0])
                    # print(buy_price)

                if Macd > signal and Macd1 < signal1:
                    if len(buy_price) > 0:
                        print("SELL")
                        print(dict1.iloc[i + 1])
                        sell_price.append(dict1.iat[(i + 1), 0])
                    # print(sell_price)
                    # print(buy_price)

        except IndexError as error:
            print("just chill")
            # print(Macd,signal,Macd1,signal1)


    get_buy_signal()


    def tradebook():
        loss = 0
        profitt = 0

        try:

            for i in range(len(buy_price)):
                # print(sell_price[i],"-",buy_price[i])
                pft = int(sell_price[i] - buy_price[i])
                if pft < 0:
                    loss += 1
                else:
                    profitt += 1
                profit.append(pft)

        except IndexError as error:
            print("just chill")
        print(len(buy_price))
        print(len(sell_price))

        print("loss trades", loss)
        print("profit trades", profitt)

        total = 0
        for i in range(len(profit)):
            total = total + profit[i]
            print("trade", i, "\t", profit[i], end="\t")
            print(total)


    tradebook()