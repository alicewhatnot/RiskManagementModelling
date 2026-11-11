"""Estimate CAPM betas for four stocks against the S&P 500.

Requires: pip install yfinance pandas numpy
"""

import yfinance as yf
import pandas as pd

STOCKS = ["AAPL", "JPM", "XOM", "KO"]
MARKET = "^GSPC"
START_DATE = "2023-01-01"
END_DATE = "2026-01-01"


def download_prices(tickers, start, end):
    """Download adjusted daily closing prices for the given tickers."""
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
    )
    return data["Close"]


def main():
    tickers = STOCKS + [MARKET]
    prices = download_prices(tickers, START_DATE, END_DATE)

    print(prices.head(12))

    # Daily percentage returns, dropping rows with missing values
    returns = prices.pct_change(fill_method=None).dropna()
    print(returns.head())

    # Market variance
    market_returns = returns[MARKET]
    market_variance = market_returns.var()
    print("Market Variance:", market_variance)

    # Apple beta (worked example)
    apple_beta = returns["AAPL"].cov(market_returns) / market_variance
    print("Apple Beta:", round(apple_beta, 4))

    # Beta for every stock
    betas = {}
    for stock in STOCKS:
        covariance = returns[stock].cov(market_returns)
        betas[stock] = covariance / market_variance

    beta_df = pd.DataFrame(list(betas.items()), columns=["Stock", "Beta"])
    beta_df["Beta"] = beta_df["Beta"].round(4)
    print(beta_df)


if __name__ == "__main__":
    main()