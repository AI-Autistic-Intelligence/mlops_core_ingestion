import yfinance as yf
import pandas as pd

def fetch_yahoo_data(ticker_symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetches historical data from Yahoo Finance and formats it for our model.
    Expected columns: 'close', 'volume'.
    """
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period, interval=interval)
    
    if df.empty:
        raise ValueError(f"No data found for ticker {ticker_symbol}")
    
    # We need 'close' and 'volume' lowercase to match our model's expectation
    df = df.rename(columns={"Close": "close", "Volume": "volume"})
    
    # Keep only relevant columns and drop NaNs
    df = df[['close', 'volume']].dropna()
    
    return df
