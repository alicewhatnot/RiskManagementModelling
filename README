# InvestSoc Quant

A small Python toolkit for measuring the risk of stocks and using those measurements to decide how much of a (pretend) fund to put in each one.

The long-term idea is a paper-trading fund that starts out split equally between its stocks, then re-weights itself according to different risk models and the combination of those models. The end goal is a dashboard where you pick any stocks and see them allocated by risk.

> **Status:** early. The risk models work and the VaR-weighted portfolio is built. Beta- and Sortino-based weighting and the combined fund are next (see [Roadmap](#roadmap)).

---

## The idea

1. **Start equal.** The fund holds four core stocks (`AAPL`, `JPM`, `XOM`, `KO`), 25% each. This is the benchmark.
2. **Measure risk.** Each model scores every stock differently.
3. **Re-weight.** Each model turns its scores into portfolio weights.
4. **Combine.** The weights from all the models are merged into one final allocation.
5. **Compare** every version against the equal-weight benchmark.

## The models

All models use daily returns from Yahoo Finance, adjusted for dividends and splits.

| Model | What it measures | File |
|---|---|---|
| **Beta** (CAPM) | How strongly a stock moves with the S&P 500. Beta = Cov(stock, market) / Var(market). Above 1 means more volatile than the market. | `beta.py` |
| **Sortino ratio** | Return per unit of *downside* risk. Like Sharpe, but only penalises returns below a target, so upside volatility isn't punished. Annualised. | `sortino.py` |
| **Historical VaR / CVaR** | VaR is the 1-day loss you'd only expect to exceed on 5% of days. CVaR is the average loss on those worst days. | `var_cvar.py` |

`var_cvar.py` also contains the portfolio comparison: equal weights against **inverse-VaR weights** (weight = 1 / VaR, scaled to sum to 100%, so lower-risk stocks get more).

## Setup

Requires Python 3.9+.

```bash
pip install yfinance pandas numpy
```

## Usage

```bash
python main.py
```

You'll be asked for a ticker:

- **Type a ticker** (e.g. `MSFT`) to get its beta, Sortino ratio, VaR, CVaR and worst day.
- **Press enter** to run the four core stocks. You also get the weights table and the equal vs VaR-weighted portfolio comparison.

Output looks like this (values omitted, they depend on the date you run it):

```
AAPL over the last 3y
  Beta vs ^GSPC:   ...
  Sortino ratio:   ...  (rf=4.0%, MAR=0.0%)
  1-day 95% VaR:   ...
  1-day 95% CVaR:  ...
  Worst day:       YYYY-MM-DD (...)

Weights:
       Equal  VaR-weighted
AAPL  25.00%           ...
...

Portfolio comparison:
                        Equal  VaR-weighted
1-day VaR 95% (loss)      ...           ...
1-day CVaR 95% (loss)     ...           ...
Annual return (gain)      ...           ...
```

## Settings

Edit the constants at the top of `main.py`:

| Constant | Default | Meaning |
|---|---|---|
| `PERIOD` | `"3y"` | Lookback window, shared by all models so results are comparable |
| `MARKET` | `"^GSPC"` | Index used as the market for beta (S&P 500) |
| `RISK_FREE_RATE` | `0.04` | Annual risk-free rate for the Sortino ratio |
| `TARGET_RETURN` | `0.0` | Annual minimum acceptable return for the Sortino ratio |
| `CONFIDENCE` | `0.95` | Confidence level for VaR / CVaR |

## Project structure

```
main.py        Entry point: asks for a ticker, runs all models, prints results
beta.py        beta(ticker, market, period)
sortino.py     sortino_ratio(ticker, period, risk_free_rate, target_return)
var_cvar.py    get_returns, var_cvar, portfolio_comparison
```

Each model is its own module with plain functions, so new models can be added without touching the others.

## Known limitations

- **Look-ahead bias.** Weights are calculated from the same data the portfolio is then tested on, so the comparison flatters the re-weighted portfolios. A proper backtest would fit weights on one period and test on the next.
- **Risk only.** Inverse-VaR weighting ignores expected returns entirely.
- **History is not a forecast.** Historical VaR assumes the next day looks like the past three years.
- **Daily rebalancing.** Portfolio returns assume fixed weights every day, with no trading costs.
- **Data quality.** Everything depends on Yahoo Finance through `yfinance`, which can have gaps or change without notice.

## Roadmap

- [x] Beta, Sortino and historical VaR / CVaR for a single ticker
- [x] Equal-weight vs inverse-VaR portfolio
- [ ] Weights from the beta model and the Sortino model (the exact rules are still to be decided, for example inverse-beta and Sortino-proportional)
- [ ] Combined weights from all models, compared against the equal-weight benchmark
- [ ] Out-of-sample testing to remove look-ahead bias
- [ ] Dashboard: choose any stocks and see them allocated by risk

## Disclaimer

This is a learning and simulation project. Nothing here is financial advice, and no real money is involved.