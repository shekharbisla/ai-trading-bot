import pandas as pd
import matplotlib.pyplot as plt
from indicators import ema, rsi, macd
from signal_engine import generate_signals

# Sample data (future me API se bhi add kar sakte ho)
data = pd.Series([100,102,101,105,110,108,112,115,117,116,120,122,121,123,125])

# Indicators
ema20 = ema(data, 20)
rsi14 = rsi(data, 14)
macd_line, signal_line = macd(data)

# Signals
signals = generate_signals(data, rsi14.fillna(50), macd_line.fillna(0), signal_line.fillna(0))

print("Trading Signals:")
for price, sig in zip(data, signals):
    print(f"Price: {price} → {sig}")

# Plot
plt.plot(data.index, data, label="Price")
plt.plot(data.index, ema20, label="EMA20")
plt.legend()
plt.title("AI Trading Bot Demo")
plt.show()
