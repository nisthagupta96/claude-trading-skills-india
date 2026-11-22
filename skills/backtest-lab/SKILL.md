---
name: backtest-lab
description: |
  Backtests rule-based swing ideas on NSE/BSE daily bars with Indian frictions built in: decide on
  the close and fill at the next open, gap-through stops, slippage, exact per-trade charges by
  segment and broker at the rates in force on each trade date, dividends, whole shares or lots,
  circuit-band no-fills, futures-only shorts, optional STCG/LTCG estimate. Six built-in strategies;
  every run is compared with buy-and-hold, a bank deposit and a Nifty 50 index fund (CAGR,
  drawdown, Sharpe/Sortino); profit factor, expectancy in ₹ and R; sweeps with a plateau-or-spike
  read, walk-forward and Monte Carlo. backtest.py, stdlib only, offline.

  Use when the user asks: "backtest this strategy", "would a 20/50 crossover have worked on X",
  "is this edge real or curve-fit", "optimise my parameters", "walk-forward test", "Monte Carlo my
  trades", "what drawdown should I expect", "do charges kill this idea", "does a NIFTY 200-DMA
  filter help", or before putting real money behind any mechanical rule.
---

# Backtest Lab

A backtest cannot prove an idea works. It can show quickly that an idea does not. Judge a rule set
by how little it degrades when Indian charges, overnight gaps, unseen years and bad luck are piled
on, and treat a spectacular first run as a reason for suspicion.

## Commands

```bash
python3 scripts/backtest.py strategies                                  # rules and defaults
python3 scripts/backtest.py run --csv tcs.csv --strategy sma-cross --params fast=20 slow=50
python3 scripts/backtest.py run --symbol POLYCAB --strategy 52w-high --risk-pct 1 --tax --trades-csv t.csv
python3 scripts/backtest.py run --csv hdfcbank.csv --strategy donchian-breakout --regime-csv nifty.csv
python3 scripts/backtest.py run --csv tcs.csv --symbol TCS --dividends auto --index-csv nifty.csv \
    --strategy donchian-breakout --deposit-rate 7
python3 scripts/backtest.py run --csv nifty.csv --strategy sma-cross --segment futures --lot-size 65 \
    --allow-short --leverage 3 --size-pct 300
python3 scripts/backtest.py sweep --csv tcs.csv --strategy sma-cross --grid fast=10,20,30 slow=50,100,200
python3 scripts/backtest.py walkforward --csv tcs.csv --strategy donchian-breakout \
    --grid entry_n=20,40,55 exit_n=10,20 --is-bars 756 --oos-bars 252
python3 scripts/backtest.py montecarlo --csv tcs.csv --strategy ema-pullback --sims 2000 --seed 7
python3 scripts/backtest.py montecarlo --from-trades t.csv --ruin-dd 25
```
Inputs follow `technical-analysis`: `--csv`, `--candles` (broker-MCP JSON, null candles skipped) or
`--symbol` (yfinance, `--period 10y`). `--start` sets the first trading day while earlier bars still
warm up the indicators. `--grid` also takes ranges (`fast=10:50:10`). Every command takes `--json`.
Bad input exits 2 with one `error:` line.

## Strategies (`--strategy`, override with `--params key=value`)

| Name | Rule (long side; shorts mirror it) | Defaults |
|---|---|---|
| sma-cross | fast SMA crosses above slow; out when back below | fast 20, slow 50, stop 3×ATR |
| ema-pullback | close above a rising trend EMA, low tags the EMA, close back above it | ema 20, trend 100, 2×ATR, target 2R, 20 bars |
| **rsi-reversion** | RSI(period) below buy_below while above the trend SMA; out above sell_above | 2, 10, 70, trend 200, 10 bars |
| donchian-breakout | close above the prior entry_n high; out below the prior exit_n low | 20 / 10, 2×ATR |
| bollinger-reversion | close below the lower band; out at the middle band | 20, k 2, trend 0 (off), 20 bars |
| 52w-high | close above the prior lookback-bar high; out below the exit SMA | 252, exit_ma 50, 2.5×ATR |

Every strategy also takes `stop_atr` (k × ATR14 from the fill), `stop_pct` (overrides it),
`target_r` and `max_hold` (bars), where 0 turns each one off. There is no custom-code hook: new
rules are added to the script as reviewed code.

## How orders and costs are simulated

- **No look-ahead.** Signals use bars up to and including the signal bar's close. The order fills at
  the next bar's open, never at the close that produced it.
- **Stops and targets** rest in the market. A gap through the level fills at the open (a stop at ₹101
  after a ₹96 open books ₹96). If one bar touches both, the stop is assumed to have filled first.
- **Slippage** `--slippage-bps` (default 5) on every fill. Use 15–30 for small caps.
- **Charges** come from `trading-costs` (charges.py) for each leg, by `--segment
  delivery|intraday|futures` and `--broker`. A delivery buy sold the same day is charged as intraday.
  Each leg pays the statutory rates in force on its own date (`RATE_HISTORY` in charges.py: STT,
  exchange charges, SEBI fee, stamp duty, GST or service tax, from June 2013), so a 2019 trade pays
  2019 STT and a 2026 futures exit pays the April 2026 STT. Broker brokerage and DP charges use
  today's pricing for every year. Eras that are approximations (NSE slab rates before Oct 2024,
  state-wise stamp duty before July 2020, the SEBI fee date, BSE rates) are listed under data notes.
  `--charge-rates current` charges today's rates throughout, for comparison.
- **Dividends** are credited in cash on the ex-date to whoever held at the previous close: a buy that
  fills on the ex-date open gets nothing. Buy-and-hold gets them the same way. They are kept as cash,
  not reinvested, and the real payment date (weeks later) is ignored. With `--symbol` they are fetched
  from yfinance; with `--csv`, pass `--dividends file.csv` (Date or Ex-Date, Dividend; per share, on the
  same split basis as the prices) or `--dividends auto` with `--symbol`. Without them the header says
  "Dividends: NOT included". Intraday trades get none. On a futures proxy (spot prices) a long is
  credited and a short debited, because real futures do not fall by the dividend on the ex-date.
- **Sizing**: `--size-pct` (default 100% of equity), `--risk-pct` (risk to the initial stop, the
  `position-sizing` method) or `--fixed-inr`. The size is set on the signal close, capped by the cash
  available at the fill, and rounded down to whole shares or whole `--lot-size` lots (futures, SME).
- **Intraday** turns each signal into a next-session open-to-close MIS trade.
- **Shorts** need `--segment futures --allow-short`. An Indian cash-market short has to be bought
  back the same session (SLB aside), so a multi-day short only exists as futures. Futures notional ≤
  equity × `--leverage`. Rollover, basis and margin calls are not modelled.
- **Circuits**: with `--circuit-band 2|5|10|20`, an open at the band limit gets no fill. The entry is
  skipped; an exit or stop waits for the next unlocked open. Each case is listed under order events.
- **Regime filter**: `--regime-csv nifty.csv` (or `--regime-symbol NIFTY`) allows longs only while the
  benchmark closes above its `--regime-ma` (200) SMA on the signal day, and shorts only below it.
- **Cash** earns nothing. Sharpe and Sortino subtract `--rf` (default 6.5% a year, about a liquid
  fund or T-bill; change it).
- **Comparison table** (every `run`, and the out-of-sample span of `walkforward`), all with the same
  capital and dates:
  - *Buy & hold*: the same stock, one delivery round trip, dividends included.
  - *Deposit*: a bank FD at `--deposit-rate` (default 6.5%) compounded quarterly, pre-tax, no risk.
  - *Nifty 50 fund*: an index fund bought at the first test day's close. Index data comes from
    `--index-csv nifty.csv` or `--index-symbol NIFTY` (automatic when prices come from yfinance).
    Yahoo's ^NSEI is a price index, so `--index-yield` (default 1.3% a year) is added for dividends;
    pass `--index-tri` if the file is the Nifty 50 TRI. `--index-ter` (default 0.2%) is deducted, plus
    0.005% stamp duty on purchase (from July 2020) and 0.001% STT on redemption. All pre-tax.
- **Dividends under `--tax`** are taxed at `--slab-pct` (they have been slab income since FY 2020-21).
- **`--tax`** applies `indian-tax-for-traders` rates for a rough post-tax view: STCG 20% (held ≤12
  months), LTCG 12.5% above ₹1.25 lakh per FY, intraday and futures at `--slab-pct`, plus 4% cess.
  It is approximate: losses are not carried forward and STT is treated as deductible, which it is not.

## Reading the output

- **Versus buy-and-hold, a deposit and the Nifty 50 fund.** A rule earns its keep with a better Sharpe
  or Calmar, or a much smaller drawdown, not just a higher return in a bull market. Two red flags are
  automatic: CAGR below the deposit (equity risk for less than an FD pays) and CAGR below the index
  fund (trading effort for less than doing nothing).
- **Max drawdown and longest underwater stretch**: would you have kept following the rules through it?
- **Profit factor** (after charges) below 1.2 is thin. Above 2 on fewer than 30 trades is suspicious.
- **Expectancy**: about +0.2R or more after costs is worth a closer look. Breakeven trades (net ₹0)
  count as neither wins nor losses and do not end a losing streak.
- **Charges as % of gross profit** above 25% means costs, not the market, own the result.
- **Yearly table**: one great year carrying the whole test is regime luck.
- **Sweep**: *plateau* (neighbours keep ≥75% of the best score) is what you want. *Slope* means pick
  the middle of the good zone. *Spike* means curve-fit. The luck hurdle is the Sharpe the best of N
  zero-edge variants would show by chance; the best cell should clear it comfortably.
- **Walk-forward**: efficiency = out-of-sample CAGR ÷ mean in-sample CAGR. ≥0.5 holds up; below 0
  fails. Frequent parameter changes mean the "optimum" is noise.
- **Monte Carlo**: size for the 95th-percentile drawdown, not the backtest's one path. *bootstrap*
  varies the outcome; *shuffle* only reorders the trades (final equity is fixed, the path is not).

## Checklist: try to break the idea before it breaks your account

1. **Look-ahead**: can every input be known before the order? Today's high/low or close cannot
   trigger an entry today. Dividend-adjusted closes are not prices anyone traded at.
2. **Survivorship**: today's NIFTY 50 or a current screener list are winners by construction. Ten
   years on them flatters every long strategy. Add names that were dropped, delisted or merged, or
   test the index itself.
3. **Overfitting**: each extra grid cell is another lottery ticket. Keep grids coarse, insist on a
   plateau, walk forward, and leave the last 1–2 years untouched until the very end.
4. **Costs**: a delivery round trip at Zerodha costs about 0.24% of the position (STT 0.1% a side,
   stamp duty, DP charge). 100 full-size round trips a year is about 24% of capital before any edge.
   High-turnover ideas die here. Rerun at 2–3× slippage and on a costlier broker.
5. **Regime**: does it only work in 2020–21-style rallies? Check the yearly rows, add `--regime-csv`,
   and include a bad phase (2008, 2015–16, 2018 small caps, March 2020, late 2024–early 2025).
6. **Data**: Yahoo history usually adjusts splits and bonuses, but not always. Moves of 25% or more
   overnight are flagged; check them. Dividends are included when the header says so; a stock that
   pays 1–3% a year makes buy-and-hold look worse than it was if they are missing.
7. **Small samples**: under 30 trades is an anecdote. Run the same rules on several stocks and look
   at the spread of results, not the best one.
8. **Execution**: thin names lock at circuits and slip more (`--circuit-band`, higher slippage). Stop
   orders are DAY-only on exchanges, so a real system needs GTTs (see `breakout-planner`).

## Workflow with other skills

1. `market-regime` (../market-regime/scripts/regime.py): test whether a NIFTY trend filter
   (`--regime-csv`) cuts drawdown more than it cuts return before using it live.
2. Run `run` → `sweep` → `walkforward` → `montecarlo`, and stop at the first red flag.
3. `position-sizing` (../position-sizing/scripts/risk.py): choose a `--risk-pct` that keeps the Monte
   Carlo 95th-percentile drawdown survivable.
4. `trading-discipline`: `--trades-csv` writes journal columns, so
   `python3 ../trading-discipline/scripts/discipline.py review t.csv` breaks the backtest down by
   weekday and setup. Compare it with your live journal later; a large gap is a warning.
5. `breakout-planner`: 52w-high and donchian-breakout are rough stand-ins for its Stage-2 entries.
   They tell you whether breakout buying pays on a stock at all, not whether a given VCP will work.

Limits: one symbol and one position at a time (no portfolio rotation), daily or weekly bars, no
options, no tick rounding.

## Output

```
NAME: strategy (params) | segment on NSE via broker | capital | sizing | slippage
start → end | bars (years) | signal on close, fill next open | charges basis | broker pricing date
Dividends: source, or NOT included
Strategy | Buy & hold | Deposit | Nifty 50 fund: total return, CAGR, max DD, volatility, Sharpe (rf),
  Sortino, Calmar, final value, dividends; deposit and index-fund basis lines
Trades N: W / L / BE | win rate | avg win / loss | PF | expectancy ₹ (R) | payoff | losing streak
Exposure | avg hold | max DD dates | longest underwater | charges (% of gross profit) | slippage
Year table (strategy, B&H, deposit, Nifty 50, trades) | last trades | order events | red flags
Data notes: dividends booked, charge-rate changes and approximations in the test window
```

_Educational analysis, not investment advice. A backtest describes the past, not your next trade._
