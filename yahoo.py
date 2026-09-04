import yfinance as yf
import pandas as pd

from .base import BaseDataClient

class YahooFinanceClient(BaseDataClient):
    def __init__(self, ticker_symbol: str, period: str = "6mo", interval: str = "1d"):
        self.ticker_symbol = ticker_symbol
        self.period = period
        self.interval = interval

    def get_dataframe(self) -> pd.DataFrame:
        """
        Fetches historical data from Yahoo Finance and formats it for our model.
        Expected columns: 'close', 'volume'.
        """
        ticker = yf.Ticker(self.ticker_symbol)
        df = ticker.history(period=self.period, interval=self.interval)
        
        if df.empty:
            raise ValueError(f"No data found for ticker {self.ticker_symbol}")
        
        df = df.rename(columns={"Close": "close", "Volume": "volume"})
        df = df[['close', 'volume']].dropna()
        
        return df

# Helper wrapper to maintain backwards compatibility
def fetch_yahoo_data(ticker_symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    client = YahooFinanceClient(ticker_symbol, period, interval)
    return client.get_dataframe()
