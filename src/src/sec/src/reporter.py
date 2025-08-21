import os
import pandas as pd
import matplotlib.pyplot as plt

def _ensure_dir(path="reports"):
    os.makedirs(path, exist_ok=True)
    return path

def save_price_chart(df: pd.DataFrame, out="reports/price_ema.png"):
    _ensure_dir(os.path.dirname(out))
    plt.figure()
    plt.plot(df.index, df["close"], label="Close")
    if "EMA20" in df.columns:
        plt.plot(df.index, df["EMA20"], label="EMA20")
    plt.title("Price & EMA20")
    plt.legend()
    plt.savefig(out, dpi=140, bbox_inches="tight")
    return out

def save_equity_chart(equity: pd.Series, out="reports/equity_curve.png"):
    _ensure_dir(os.path.dirname(out))
    plt.figure()
    plt.plot(equity.index, equity.values, label="Equity")
    plt.title("Equity Curve")
    plt.legend()
    plt.savefig(out, dpi=140, bbox_inches="tight")
    return out

def export_trades(trades_df: pd.DataFrame, out="reports/trades.csv"):
    _ensure_dir(os.path.dirname(out))
    trades_df.to_csv(out, index=False)
    return out
