import pylab, random

class Stock:
    def __init__(self, ticker, volatility, price):
        self.volatility = volatility
        self.ticker = ticker
        self.price = price
    def setPrice(self, price):
        self.price = price
    def makeMove(self, bias):
        baseMove = random.gauss(0, 0.02)
        self.price = self.price * (1.0 + baseMove + bias)
        if self.price < 0.01:
            self.price = 0.0
    def getPrice(self):
        return self.price
    def getTicker(self):
        return self.ticker

class Market:
    def __init__(self, price):
        self.tickers = set()
        self.stocks = []
        self.startPrice = price
        self.history = {}
        self.averages = []
    def addStock(self, stk):
        if stk.getTicker() in self.tickers:
            raise 'ValueError'
        self.tickers.add(stk.getTicker())
        self.stocks.append(stk)
        self.history[stk.getTicker()] = [self.startPrice]
    def makeMove(self, bias):
        tot = 0
        for s in self.stocks:
            s.makeMove(bias)
            self.history[s.getTicker()].append(s.getPrice())
            tot += s.getPrice()
        self.averages.append(tot/len(self.stocks))
    def getStocks(self):
        return self.stocks
    def getStartPrice(self):
        return self.startPrice
    def getHistory(self):
        return self.history
    def getAverages(self):
        return self.averages[:]

def generateMkt(n, maxVol, startPrice):
    mkt = Market(startPrice)
    for i in range(n):
        ticker = str(i)
        volatility = random.uniform(0, maxVol)
        stk = Stock(ticker, volatility, startPrice)
        mkt.addStock(stk)
    return mkt

def simMkt(mkt, numDays):
    for d in range(numDays):
        mktBias = random.gauss(0.04/200, 0.25/200)
        mkt.makeMove(mktBias)
        
def analyzeSim(mkt):
    history = mkt.getHistory()
    lastSales = []
    for k in history:
        pylab.plot(history[k])
        lastSales.append(history[k][-1])
    pylab.semilogy()
    pylab.title('Daily Closing Prices')
    pylab.xlabel('Stock')
    pylab.ylabel('Price')
    pylab.figure()
    pylab.hist(lastSales, bins = 40)
    ave = sum(lastSales)/len(lastSales)
    pylab.axvline(ave, color = 'r', label = 'Market Average')
    pylab.legend()
    pylab.title('Distribution of Last Sales')
    pylab.xlabel('Last Sale')
    pylab.ylabel('Number of Securities')
    pylab.figure()
    pylab.plot(mkt.getAverages())
    pylab.title('Market Average')
    pylab.ylabel('Average Price')
    pylab.xlabel('Day from Start')

    
startPrice = 100
maxVol = 0.1 #10%/day 
random.seed(1) 
mkt = generateMkt(500, maxVol, startPrice)
simMkt(mkt, 10*200)
analyzeSim(mkt)
