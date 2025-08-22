# AI Trading Bot 🤖📈

An **international-level open-source project** to showcase Python, AI, and Finance skills.  
The bot fetches live market data, calculates indicators, generates signals, and runs a simple backtest with reports.

---

## ✨ Features
- Real-time crypto market data (Binance public API)
- Technical indicators: **EMA, RSI, MACD**
- Rule-based **Buy / Sell / Hold** signal engine
- Simple backtester (PnL, Win Rate, Drawdown)
- Charts & CSV reports auto-saved in `/reports`
- Clean, modular Python code structure
- Unit tests + GitHub Actions CI (professional repo standards)

---

## 🧰 Tech Stack
- **Python 3.11**
- Pandas, NumPy
- Matplotlib
- scikit-learn
- Requests (API)
- FastAPI + Uvicorn (for optional REST API)
- Pytest (for testing)

---

## 📦 Project Structure

ai-trading-bot/
├─ src/
│   ├─ indicators.py      # EMA, RSI, MACD
│   ├─ signal_engine.py   # Buy/Sell/Hold rules
│   ├─ data_fetch.py      # Binance OHLCV data
│   ├─ backtester.py      # Simple PnL & equity calc
│   ├─ reporter.py        # Charts & CSV exports
│   ├─ runner.py          # Main orchestration script
│   └─ api.py             # (Optional) REST API
├─ tests/                 # Pytest unit tests
├─ reports/               # Auto-generated reports
├─ requirements.txt
└─ README.md

---
## 🚀 Quick Start (Backtest Demo)
```bash
pip install -r requirements.txt
python -m src.runner
This will:
	•	Fetch BTCUSDT 1h candles from Binance public API
	•	Calculate indicators (EMA, RSI, MACD)
	•	Generate Buy/Sell/Hold signals
	•	Run a simple backtest
	•	Save reports:
	•	reports/price_ema.png
	•	reports/equity_curve.png
	•	reports/trades.csv
