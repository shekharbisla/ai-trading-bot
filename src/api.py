from fastapi import FastAPI, Query
from typing import List, Dict, Any

from data_fetch import fetch_klines
from indicators import ema, rsi, macd
from signal_engine import generate_signals
from backtester import backtest
from reporter import save_price_chart, save_equity_chart, export_trades

app = FastAPI(title="AI Trading Bot API", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/signals")
def signals(
    symbol: str = Query("BTCUSDT", min_length=6, max_length=15),
    interval: str = Query("1h"),
    limit: int = Query(150, ge=50, le=1000),
) -> List[Dict[str, Any]]:
    """
    Returns last N candles with indicators + text signals.
    """
    df = fetch_klines(symbol=symbol, interval=interval, limit=limit)
    close = df["close"]

    df["EMA20"] = ema(close, 20)
    df["RSI14"] = rsi(close, 14)
    m_line, s_line = macd(close)
    df["MACD"], df["SIGNAL"] = m_line, s_line

    df["SIGNAL_TXT"] = generate_signals(
        close.values,
        df["RSI14"].fillna(50).values,
        df["MACD"].fillna(0).values,
        df["SIGNAL"].fillna(0).values,
    )

    return df.to_dict(orient="records")


@app.get("/backtest")
def backtest_summary(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    limit: int = Query(500, ge=100, le=1000),
    save_reports: bool = Query(True),
) -> Dict[str, Any]:
    """
    Runs end-to-end: data → indicators → signals → backtest.
    Optionally saves charts/CSV to reports/.
    """
    df = fetch_klines(symbol=symbol, interval=interval, limit=limit)
    df = df.set_index("open_time")
    close = df["close"]

    # indicators
    df["EMA20"] = ema(close, 20)
    df["RSI14"] = rsi(close, 14)
    m_line, s_line = macd(close)
    df["MACD"], df["SIGNAL"] = m_line, s_line

    # signals
    df["SIGNAL_TXT"] = generate_signals(
        close.values,
        df["RSI14"].fillna(50).values,
        df["MACD"].fillna(0).values,
        df["SIGNAL"].fillna(0).values,
    )

    # backtest
    summary, equity, trades_df = backtest(df, price_col="close", signal_col="SIGNAL_TXT")

    files = {}
    if save_reports:
        files["price_chart"] = save_price_chart(df, out="reports/price_ema.png")
        files["equity_chart"] = save_equity_chart(equity, out="reports/equity_curve.png")
        files["trades_csv"] = export_trades(trades_df, out="reports/trades.csv")

    # compact response
    return {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "summary": summary,
        "reports": files,
    }
