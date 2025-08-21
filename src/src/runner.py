import os
import pandas as pd
from data_fetch import fetch_klines
from indicators import ema, rsi, macd
from signal_engine import generate_signals
from backtester import backtest
from reporter import save_equity_chart, save_price_chart, export_trades

def main():
    # 1) Data: BTCUSDT 1h (public API)
    df = fetch_klines(symbol="BTCUSDT", interval="1h", limit=500)
    df = df.set_index("open_time")
    close = df["close"]

    # 2) Indicators
    df["EMA20"] = ema(close, 20)
    df["RSI14"] = rsi(close, 14)
    m_line, s_line = macd(close)
    df["MACD"] = m_line
    df["SIGNAL"] = s_line

    # 3) Signals
    df["SIGNAL_TXT"] = generate_signals(
        close.values,
        df["RSI14"].fillna(50).values,
        df["MACD"].fillna(0).values,
        df["SIGNAL"].fillna(0).values
    )

    # 4) Backtest
    summary, equity, trades_df = backtest(df, price_col="close", signal_col="SIGNAL_TXT")
    print("Backtest summary:", summary)

    # 5) Reports (charts + CSV saved to reports/)
    os.makedirs("reports", exist_ok=True)
    p1 = save_price_chart(df, out="reports/price_ema.png")
    p2 = save_equity_chart(equity, out="reports/equity_curve.png")
    p3 = export_trades(trades_df, out="reports/trades.csv")
    print(f"Saved: {p1}, {p2}, {p3}")

if __name__ == "__main__":
    main()
