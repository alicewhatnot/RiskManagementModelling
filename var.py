"""Historical VaR / CVaR per stock, plus equal-weight vs inverse-VaR portfolios."""

import pandas as pd
import yfinance as yf

TRADING_DAYS = 252


def get_returns(tickers: list[str], period: str = "3y") -> pd.DataFrame:
    """Daily % returns for each ticker (adjusted for dividends and splits)."""
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    if data is None or data.empty:
        raise ValueError(f"No price data found for {', '.join(tickers)}")

    prices = pd.DataFrame(data["Close"])
    missing = [t for t in tickers if t not in prices.columns or prices[t].dropna().empty]
    if missing:
        raise ValueError(f"No price data found for {', '.join(missing)}")

    # dropna removes the first day (no yesterday to compare with)
    return prices.pct_change(fill_method=None).dropna()


def var_cvar(returns: pd.DataFrame, confidence: float = 0.95) -> pd.DataFrame:
    """1-day historical VaR and CVaR per column, as positive loss fractions.

    VaR:  cut-off of the worst (1 - confidence) of days. 2.33% means that on
          95% of days the loss is smaller than 2.33%.
    CVaR: average return on the days at or beyond the VaR cut-off, so it is
          always bigger than VaR and shows how bad the bad days get.
    """
    var = -returns.quantile(1 - confidence)
    cvar = pd.Series(
        {col: -returns[col][returns[col] <= -var[col]].mean() for col in returns.columns}
    )
    return pd.DataFrame({"VaR": var, "CVaR": cvar})


def portfolio_comparison(
    returns: pd.DataFrame, confidence: float = 0.95
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Equal-weight benchmark vs inverse-VaR weights.

    Inverse-VaR: weight = (1 / VaR), scaled to sum to 100%, so lower-risk
    stocks get more weight. It looks at risk only and ignores returns.
    Weights are fitted on the same data they are tested on (look-ahead bias).

    Returns (weights, results). Compare across columns, not rows, since the
    rows mix a daily loss with a yearly gain.
    """
    stats = var_cvar(returns, confidence)
    n = len(returns.columns)

    equal_weights = pd.Series(1 / n, index=returns.columns)
    inv_var = 1 / stats["VaR"]
    var_weights = inv_var / inv_var.sum()

    weights = pd.DataFrame({"Equal": equal_weights, "VaR-weighted": var_weights})

    # Fixed weights every day (daily rebalancing)
    portfolios = {
        "Equal": (returns * equal_weights).sum(axis=1),
        "VaR-weighted": (returns * var_weights).sum(axis=1),
    }

    results = {}
    for name, port in portfolios.items():
        p_var = -float(port.quantile(1 - confidence))
        p_cvar = -float(port[port <= -p_var].mean())
        p_annual = float(port.mean()) * TRADING_DAYS  # rough yearly return
        results[name] = [p_var, p_cvar, p_annual]

    results_df = pd.DataFrame(
        results,
        index=[
            f"1-day VaR {confidence:.0%} (loss)",
            f"1-day CVaR {confidence:.0%} (loss)",
            "Annual return (gain)",
        ],
    )
    return weights, results_df