"""CAPM beta of a stock against a market index."""

import pandas as pd
import yfinance as yf


def beta(ticker: str, market: str = "^GSPC", period: str = "3y") -> float:
    """Beta = Cov(stock, market) / Var(market), using daily returns."""
    data = yf.download(
        [ticker, market],
        period=period,
        auto_adjust=True,
        progress=False,
    )
    # yf.download is typed as Optional, so check before subscripting
    if data is None or data.empty:
        raise ValueError(f"No price data found for '{ticker}'")

    prices = pd.DataFrame(data["Close"])
    if ticker not in prices.columns or prices[ticker].dropna().empty:
        raise ValueError(f"No price data found for '{ticker}'")

    returns: pd.DataFrame = prices.pct_change(fill_method=None).dropna()
    stock: pd.Series = returns[ticker]
    mkt: pd.Series = returns[market]

    return float(stock.cov(mkt) / mkt.var())