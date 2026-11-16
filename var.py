# Historical VaR – InvestSoc Quant
# Risk metric: 1-day historical VaR (+ CVaR) for AAPL, JPM, XOM, KO
# Portfolio: inverse-VaR weights vs equal 25% x 4 benchmark
# Data: Yahoo Finance

import pandas as pd
import yfinance as yf

# ----- SETTINGS -----
tickers = ["AAPL", "JPM", "XOM", "KO"] # stock tickers
start_date = "2023-01-01" # team-agreed start
end_date = pd.Timestamp.today().strftime("%Y-%m-%d") # end is exclusive -> data up to yesterday
confidence = 0.95 # everyday standard: stable + testable

# ----- DATA -----
# daily closing prices from Yahoo Finance
# auto_adjust=True -> adjusts for dividends + stock splits (matters for KO, XOM)
prices = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]

# TESTS
print("Prices of the first 5 days:")
print(prices.head())
print(" ")

print("Prices of the 5 latest days:")
print(prices.tail())
print(" ")

# ----- RETURNS -----
# daily % change: (today - yesterday) / yesterday
# dropna -> removes the first day (since there is no yesterday)
returns = prices.pct_change().dropna()

# TESTS
print("Returns of the first 5 rows:")
print(returns.head())
print(" ")

print("Statistics summary:")
print(returns.describe()) # count, mean, std (volatility), min (worst day), percentiles, max (best day)
print(" ")

print("Date of each stock's worst day:")
print(returns.idxmin())
print(" ")

# ----- VaR -----
# quantile(0.05) -> cut-off of the worst 5% of days
# minus sign -> shows the loss as a positive number
# e.g. 2.33% -> on 95% of days, the loss is smaller than 2.33%
var = -returns.quantile(1 - confidence).rename("VaR")

print("1-day 95% historical VaR:")
print(var.map("{:.2%}".format))
print(" ")

# ----- CVaR (Expected Shortfall) -----
# keep only days at or beyond the VaR cut-off, then average them
# minus sign -> shows the loss as a positive number
# always bigger than VaR -> shows how bad the bad days get
worst_days = returns[returns <= -var]
cvar = -worst_days.mean().rename("CVaR")

print("1-day 95% historical CVaR:")
print(cvar.map("{:.2%}".format))
print(" ")

# ----- PORTFOLIOS (equal 25% x 4 vs inverse-VaR) -----
# equal -> 25% in each stock (benchmark)
# inverse-VaR -> 1 / VaR, scaled to add up to 100% (lower risk = more weight)
# note: looks at risk only, ignores returns
equal_weights = pd.Series(0.25, index=tickers)
var_weights = (1 / var) / (1 / var).sum()

print("Weights:")
weights = pd.DataFrame({"Equal": equal_weights, "VaR-weighted": var_weights})
print(weights.map("{:.2%}".format))
print(" ")

# portfolio daily return = weight x return for each stock, added across the row
# assumes fixed weights every day (daily rebalancing)
equal_returns = (returns * equal_weights).sum(axis=1)
var_port_returns = (returns * var_weights).sum(axis=1)

# ----- PORTFOLIO RISK + RETURN -----
# same VaR / CVaR formulas, applied to the portfolio
# lower than single stocks -> diversification (stocks don't all crash together)
equal_var = -equal_returns.quantile(1 - confidence)
var_port_var = -var_port_returns.quantile(1 - confidence)

equal_cvar = -equal_returns[equal_returns <= -equal_var].mean()
var_port_cvar = -var_port_returns[var_port_returns <= -var_port_var].mean()

# average daily return x 252 trading days -> rough yearly return
equal_annual = equal_returns.mean() * 252
var_port_annual = var_port_returns.mean() * 252

results = pd.DataFrame({
    "Equal 25% x 4": [equal_var, equal_cvar, equal_annual],
    "VaR-weighted": [var_port_var, var_port_cvar, var_port_annual],
}, index=["1-day VaR 95% (loss)", "1-day CVaR 95% (loss)", "Annual return (gain)"])

# compare across columns, not rows (daily loss vs yearly gain)
# caveat: weights use the same data they're tested on (look-ahead bias)
print("Portfolio comparison:")
print(results.map("{:.2%}".format))
