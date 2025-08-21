from dataclasses import dataclass
from typing import List, Optional
import pandas as pd

@dataclass
class Trade:
    entry_time: pd.Timestamp
    entry_price: float
    side: str  # "LONG" or "SHORT"
    exit_time: Optional[pd.Timestamp] = None
    exit_price: Optional[float] = None
    pnl: Optional[float] = None

def backtest(df: pd.DataFrame, price_col: str = "close", signal_col: str = "SIGNAL_TXT"):
    """
    Simple backtest:
    - BUY  => open/hold one LONG until SELL
    - SELL => open/hold one SHORT until BUY
    - HOLD => no change
    Position size = 1 unit
    """
    price = df[price_col].values
    time = df.index
    sigs = df[signal_col].values

    equity_curve = []
    trades: List[Trade] = []
    position = None  # tuple: (side, entry_idx, entry_price)
    realized_pnl = 0.0

    for i in range(len(df)):
        s = sigs[i]
        p = float(price[i])

        # switch/open/close logic
        if s == "BUY":
            if position and position[0] == "SHORT":
                entry_idx = position[1]
                pnl = (position[2] - p)  # short: entry - exit
                realized_pnl += pnl
                trades.append(Trade(time[entry_idx], float(price[entry_idx]), "SHORT", time[i], p, pnl))
                position = None
            if not position:
                position = ("LONG", i, p)

        elif s == "SELL":
            if position and position[0] == "LONG":
                entry_idx = position[1]
                pnl = (p - position[2])  # long: exit - entry
                realized_pnl += pnl
                trades.append(Trade(time[entry_idx], float(price[entry_idx]), "LONG", time[i], p, pnl))
                position = None
            if not position:
                position = ("SHORT", i, p)

        # mark-to-market equity
        if not position:
            equity_curve.append(realized_pnl)
        else:
            side, entry_idx, entry_price = position
            if side == "LONG":
                equity_curve.append(realized_pnl + (p - entry_price))
            else:
                equity_curve.append(realized_pnl + (entry_price - p))

    # force close at last bar
    if position:
        side, entry_idx, entry_price = position
        p = float(price[-1])
        pnl = (p - entry_price) if side == "LONG" else (entry_price - p)
        realized_pnl += pnl
        trades.append(Trade(time[entry_idx], float(price[entry_idx]), side, time[-1], p, pnl))

    equity = pd.Series(equity_curve, index=df.index, name="equity")

    wins = sum(1 for t in trades if (t.pnl or 0) > 0)
    total = len(trades)
    summary = {
        "trades": total,
        "total_pnl": round(float(realized_pnl), 4),
        "win_rate": round(100 * wins / total, 2) if total else 0.0,
        "max_drawdown": round(float((equity.cummax() - equity).max() or 0), 4)
    }

    trades_df = pd.DataFrame([t.__dict__ for t in trades])
    return summary, equity, trades_df
