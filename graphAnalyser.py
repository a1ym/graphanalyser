import yfinance as yf
from datetime import datetime, timedelta
import io
import sys
import pandas as pd
import plotly.graph_objs as go
import numpy as np


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

candles = []

class candle():
    def __init__(self, hi, lo, open, close):
        self.hi = hi
        self.lo = lo
        self.open = open
        self.close = close




# Function that makes candle objects
def candleObj(hi, lo, open, close):
    candles = []
    for i in range(len(open)):
        candles.append(candle(hi[i], lo[i], open[i], close[i]))
    return candles

# Function that returns current data of forex
def current(prd, intr):
    data = yf.download(tickers = 'EURUSD=X', period = prd, interval = intr)
    print("*****" + data["Open"])
    return data





# Function that returns a list of "type" values.
def listOfVal(data, type):
    s = io.StringIO(str(data[type]))
    lst = []
    for line in s:
        if "    " not in line:
            continue
        a = (str(line.split("    ", 1)[1]))
        lst.append(a)
    return lst



# Function that creates an object graph out of forex data
def graphObj(data):
    hi = listOfVal(data, "High")
    lo = listOfVal(data, "Low")
    open = listOfVal(data, "Open")
    close = listOfVal(data, "Close")
    graph = candleObj(hi, lo, open, close)
    return graph






# Function that calculates percentage difference of 2 values given.
def diff(a, b):
    c = (((float(b) / float(a)) - 1) * 100)
    return c


# Function that compares 2 graphs and returns their difference
def compare(graph1, graph2):
    try:
        base1 = graph1[0].open
        base2 = graph2[0].open
        totalDiff = 0
        for i in range(0, len(graph1)):
            openDiff = abs(diff(base1, graph1[i].open) - diff(base2, graph2[i].open))
            hiDiff = abs(diff(base1, graph1[i].hi) - diff(base2, graph2[i].hi))
            loDiff = abs(diff(base1, graph1[i].lo) - diff(base2, graph2[i].lo))
            closeDiff = abs(diff(base1, graph1[i].close) - diff(base2, graph2[i].close))
            totalDiff = totalDiff + openDiff + hiDiff + loDiff + closeDiff
    except Exception as e:
        #print(e)
        return 0
    return totalDiff



def plotCandle(fig, data, date, c1, c2):
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market on ' + str(date), increasing_line_color = c1, decreasing_line_color = c2))

#def plotLine(fig, data, date, c1):
#    fig.add_trace(go.layout.shape.Line(x=data.index, y=data['Open'], name = 'market on ' + str(date), line = dict(color = c1)))




def startCompare(start_date, end_date, tickr, prd, intr):
    #currentData = yf.download(tickers = 'EURUSD=X', period = str(prd) + "d", interval = "1h")
    currentData = yf.download(tickers = "EURUSD=X", start=datetime(2021, 8, 26, 22), end=datetime(2021, 8, 27, 22), interval = "60m")
    currentGraph = graphObj(currentData)
    fig = go.Figure()
    results = []
    dates = []
    start = ""
    end = " "
    delta = timedelta(days=prd)
    output = 1
    print("Loading...")
    while start != end_date.strftime("%Y-%m-%d"):
        while start_date <= end_date:
            start = start_date.strftime("%Y-%m-%d")
            end = start_date + delta
            end = end.strftime("%Y-%m-%d")
            historyData = yf.download(tickr, start=start, end=end, interval = intr)
            historyGraph = graphObj(historyData)
            output = compare(currentGraph, historyGraph)
            if output > 0:
                results.append(output)
                dates.append(start_date)
            start_date += delta


    #for i in range(0, len(results)):
        #a = str(results[i]) + "% Diff on dates: " + str(dates[i])
        #print(a)

    #colours = ["black", "black", "black", "black", "black"]
    top5 = []
    for i in range(0, 5):
        indexMin = results.index(min(results))
        top = str(min(results)) + "% on " + str(dates[indexMin].strftime("%Y-%m-%d"))
        data = yf.download(tickr, start=dates[indexMin], end=dates[indexMin] + timedelta(days=1), interval = intr)
        plotCandle(fig, data, dates[indexMin].strftime("%Y-%m-%d"), "red", "green")
        data2 = yf.download(tickr, start=dates[indexMin] + timedelta(days=1), end=dates[indexMin] + timedelta(days=5), interval = intr)
        plotCandle(fig, data2, "", "blue", "blue")
        top5.append(top)
        results.pop(indexMin)
        dates.pop(indexMin)




    print("\n\n\nTHE MINIMUM DIFFERENCE IS", min(results), "%")
    print("ON THE DATE", dates[results.index(min(results))].strftime("%Y-%m-%d"))
    print("\n\n\n")

    print("TOP 5 VALUES:")
    for i in range(0, len(top5)):
        print(top5[i])

    plotCandle(fig, currentData, "", "red", "red")
    fig.show()








    #Function that will find most identical graph
    #plot(currentData, historyData)
    #print(compare(currentGraph, historyGraph))



startCompare(datetime(2020, 1, 1), datetime(2021, 8, 20), "EURUSD=X", 1, "1h")



#Need to make it so bigger graphs can be compared with smaller
#And need to make so you can choose how big is the "compareto" graph (2d, 3d...)
