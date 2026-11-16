"""Run CAPM beta and Sortino ratio on a ticker chosen by the user.

Requires: pip install yfinance pandas numpy
"""

from beta import beta
from sortino import sortino_ratio

PERIOD = "3y"
MARKET = "^GSPC"
RISK_FREE_RATE = 0.04
TARGET_RETURN = 0.0


def main():
    ticker = input("Enter a ticker (e.g. AAPL): ").strip().upper()
    if not ticker:
        print("No ticker entered.")
        return

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
        return

    print(f"\n{ticker} over the last {PERIOD}")
    print(f"  Beta vs {MARKET}: {b:.4f}")
    print(f"  Sortino ratio:   {s:.2f}  (rf={RISK_FREE_RATE:.1%}, MAR={TARGET_RETURN:.1%})")


if __name__ == "__main__":
    main()