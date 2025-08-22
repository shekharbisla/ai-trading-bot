import pandas as pd
from src.indicators import ema, rsi, macd
from src.signal_engine import generate_signals
from src.backtester import backtest

def test_indicators_shapes():
    s = pd.Series(range(1, 60))
    e = ema(s, 10)
    r = rsi(s, 14)
    m, sig = macd(s)
    assert len(e) == len(s)
    assert len(r) == len(s)
    assert len(m) == len(sig) == len(s)

def test_signal_engine_basic():
    prices = pd.Series([1,2,3,4,5,6,7,8,9,10]).values
    rsi_vals = pd.Series([20,25,40,50,80,75,60,55,45,35]).values
    macd_line = pd.Series([1,1,1,1,0,-1,-1,-1,0,1]).values
    signal_line = pd.Series([0,0,0,0,0,0,0,0,0,0]).values
    sigs = generate_signals(prices, rsi_vals, macd_line, signal_line)
    assert len(sigs) == len(prices)

def test_backtest_runs():
    df = pd.DataFrame({"close":[100,101,102,101,99,98,99,100,101,103]})
    df.index = pd.date_range("2024-01-01", periods=len(df), freq="H")
    df["SIGNAL_TXT"] = ["BUY","HOLD","HOLD","SELL","HOLD","HOLD","BUY","HOLD","HOLD","SELL"]
    summary, equity, trades = backtest(df)
    assert "total_pnl" in summary
    assert len(equity) == len(df)
