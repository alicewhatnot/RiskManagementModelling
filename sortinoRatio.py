import numpy as np
import yfinance as yf


def sortino_ratio(
    ticker: str,
    period: str = "3y",
    risk_free_rate: float = 0.04,   # annual, e.g. 0.04 = 4%
    target_return: float = 0.0,     # annual minimum acceptable return (MAR)
    periods_per_year: int = 252,
) -> float:
    
    """Annualised Sortino ratio for a ticker using daily returns."""
    prices = yf.Ticker(ticker).history(period=period, auto_adjust=True)["Close"]
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise ValueError(f"No price data found for '{ticker}'")

    # Convert annual rates to per-period rates
    rf_daily = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    mar_daily = (1 + target_return) ** (1 / periods_per_year) - 1

    excess = returns - rf_daily
    downside = np.minimum(returns - mar_daily, 0)
    downside_dev = np.sqrt(np.mean(downside ** 2))  # over ALL periods, not just negative ones

    if downside_dev == 0:
        return float("nan")

    return float(excess.mean() / downside_dev * np.sqrt(periods_per_year))



print(f"AAPL Sortino: {sortino_ratio('AAPL', '3y', 0.04, 0.2):.2f}")