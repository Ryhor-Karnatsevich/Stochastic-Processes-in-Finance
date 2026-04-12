import yfinance as yf
from datetime import datetime, timedelta

class Data:
    def __init__(self, ticker):
        self.ticker = ticker
        self.start = datetime.now().date() - timedelta(days=1000)
        self.data = None

    def load(self):
        self.data = yf.download(self.ticker, start=self.start)
        return self.data
