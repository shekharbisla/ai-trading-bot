def generate_signals(prices, rsi_vals, macd_line, signal_line):
    """Basic strategy rules:
    - Buy when RSI < 30 and MACD > Signal
    - Sell when RSI > 70 and MACD < Signal
    """
    signals = []
    for i in range(len(prices)):
        if rsi_vals[i] < 30 and macd_line[i] > signal_line[i]:
            signals.append("BUY")
        elif rsi_vals[i] > 70 and macd_line[i] < signal_line[i]:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals
