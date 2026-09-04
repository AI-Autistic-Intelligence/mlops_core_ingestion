# MLOps Core Ingestion

A centralized repository for data ingestion clients (Yahoo Finance, Binance Websockets, etc.).

## Usage
All clients inherit from `BaseDataClient` and implement `get_dataframe()`.

```python
from mlops_core_ingestion.yahoo import YahooFinanceClient
from mlops_core_ingestion.binance_ws import BinanceWSClient

# Polling
client = YahooFinanceClient("AAPL")
df = client.get_dataframe()

# Streaming
ws = BinanceWSClient("btcusdt")
ws.start()
live_df = ws.get_dataframe()
```
