import json
import threading
import websocket
import pandas as pd

from .base import BaseDataClient

class BinanceWSClient(BaseDataClient):
    """
    A simple WebSocket client that connects to Binance and buffers the latest
    price and volume data in memory. Runs in a daemon thread.
    """
    def __init__(self, symbol="btcusdt", interval="1m", max_buffer=200):
        self.symbol = symbol.lower()
        self.interval = interval
        self.max_buffer = max_buffer
        self.url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"
        self.data_buffer = []
        self.ws = None
        self.thread = None
        self.is_running = False

    def on_message(self, ws, message):
        data = json.loads(message)
        kline = data['k']
        
        timestamp = pd.to_datetime(kline['t'], unit='ms')
        close = float(kline['c'])
        volume = float(kline['v'])
        
        # Update current candle or append new one
        if len(self.data_buffer) > 0 and self.data_buffer[-1]['timestamp'] == timestamp:
            self.data_buffer[-1] = {'timestamp': timestamp, 'close': close, 'volume': volume}
        else:
            self.data_buffer.append({'timestamp': timestamp, 'close': close, 'volume': volume})
            
        # Maintain buffer size
        if len(self.data_buffer) > self.max_buffer:
            self.data_buffer = self.data_buffer[-self.max_buffer:]

    def on_error(self, ws, error):
        print(f"WS Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WS Closed")
        self.is_running = False

    def on_open(self, ws):
        print(f"WS Opened for {self.symbol}")
        self.is_running = True

    def start(self):
        if not self.is_running:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self.thread.start()

    def get_dataframe(self):
        if not self.data_buffer:
            return pd.DataFrame(columns=['close', 'volume'])
        df = pd.DataFrame(self.data_buffer)
        df.set_index('timestamp', inplace=True)
        return df
