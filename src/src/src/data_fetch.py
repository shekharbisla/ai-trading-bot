import time
import requests
import pandas as pd

BINANCE_BASE = "https://api.binance.com/api/v3/klines"

def fetch_klines(symbol="BTCUSDT", interval="1h", limit=500):
    """
    Fetch OHLCV from Binance public API (no key needed).
    Returns pandas.DataFrame with columns: open_time, open, high, low, close, volume
    """
    url = BINANCE_BASE
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    cols = ["open_time","open","high","low","close","volume",
            "close_time","qav","num_trades","taker_base_vol","taker_quote_vol","ignore"]
    df = pd.DataFrame(data, columns=cols)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)
    return df[["open_time","open","high","low","close","volume"]]
