import pandas as pd

def ema(data: pd.Series, period: int = 14):
    """Exponential Moving Average"""
    return data.ewm(span=period, adjust=False).mean()

def rsi(data: pd.Series, period: int = 14):
    """Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(data: pd.Series, fast=12, slow=26, signal=9):
    """Moving Average Convergence Divergence"""
    fast_ema = ema(data, fast)
    slow_ema = ema(data, slow)
    macd_line = fast_ema - slow_ema
    signal_line = ema(macd_line, signal)
    return macd_line, signal_line
