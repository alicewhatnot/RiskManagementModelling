"""Run CAPM beta, Sortino ratio and historical VaR/CVaR on a ticker.

With the default tickers it also compares an equal-weight portfolio against
an inverse-VaR-weighted one.

Requires: pip install yfinance pandas numpy
"""

from beta import beta
from sortino import sortino_ratio
from var import get_returns, portfolio_comparison, var_cvar

PERIOD = "3y"
MARKET = "^GSPC"
RISK_FREE_RATE = 0.04
TARGET_RETURN = 0.0
CONFIDENCE = 0.95


def main():
    ticker = input("Enter a ticker (e.g. AAPL) or enter to use default tickers: ").strip().upper()
    if not ticker:
        print("Evaluating core 4 stocks.")
        tickers = ["AAPL", "JPM", "XOM", "KO"]
    else:
        tickers = [ticker]

    try:
        returns = get_returns(tickers, period=PERIOD)
    except ValueError as e:
        print(f"Error: {e}")
        return
    risk = var_cvar(returns, CONFIDENCE)
    worst_days = returns.idxmin()

    for ticker in tickers:
        try:
            b = beta(ticker, market=MARKET, period=PERIOD)
            s = sortino_ratio(
                ticker,
                period=PERIOD,
                risk_free_rate=RISK_FREE_RATE,
                target_return=TARGET_RETURN,
            )
        except ValueError as e:
            print(f"Error: {e}")
            continue

        worst = worst_days[ticker]
        print(f"\n{ticker} over the last {PERIOD}")
        print(f"  Beta vs {MARKET}: {b:.4f}")
        print(f"  Sortino ratio:   {s:.2f}  (rf={RISK_FREE_RATE:.1%}, MAR={TARGET_RETURN:.1%})")
        print(f"  1-day {CONFIDENCE:.0%} VaR:   {risk.loc[ticker, 'VaR']:.2%}")
        print(f"  1-day {CONFIDENCE:.0%} CVaR:  {risk.loc[ticker, 'CVaR']:.2%}")
        print(f"  Worst day:       {worst:%Y-%m-%d} ({returns.loc[worst, ticker]:.2%})")

    if len(tickers) > 1:
        weights, results = portfolio_comparison(returns, CONFIDENCE)
        print("\nWeights:")
        print(weights.map("{:.2%}".format))
        print("\nPortfolio comparison:")
        print(results.map("{:.2%}".format))


if __name__ == "__main__":
    main()