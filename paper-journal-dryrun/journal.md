# Paper-trading journal: DRY RUN (practice run for Monday 23 Nov 2026)

> **DRY RUN.** This was made on Sunday 22 Nov to test the morning task. It is not the real journal (`paper-journal/`).
> **SIMULATION ONLY: no real orders. Prices are from delayed Yahoo Finance (Friday 20 Nov close).**

Starting date: 2026-11-23 (dry run)

Fixed rules:
- ₹10,000 per stock.
- Stop = entry − 2×ATR.
- Target = 2× the risk.
- Max 3 stocks at once.
- Max 20 trading days per trade.
- Skip if it opens more than 3% above the buy price.

## Open positions

| Date | Stock | Status | Entry | Stop | Target | Qty | Invested ₹ | ATR |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | BAJFINANCE | PLANNED | 1,129.20 | 1,068.60 | 1,250.40 | 8 | 9,033.60 | 30.30 |

*In words: one pretend trade is planned and nothing has been bought yet. We buy 8 Bajaj Finance shares only if the price rises to ₹1,129.20.*

## Cumulative net P&L since start
Realised: ₹0.00 · Unrealised: ₹0.00

## Lessons covered

## Daily log

### 2026-11-23 Morning (dry run, using Friday 20 Nov data)

**Market view**
- **The market is in a "confirmed uptrend".** This is the market-regime tool's label for "the NIFTY 50 is clearly rising, so it is a normal time to buy". NIFTY 50 is the index of India's 50 biggest companies, the one a Nifty index fund copies.
  - It closed Friday at 25,801, up 1.1%, just 2.2% below its high for the year.
  - There have been 0 heavy-selling days in the last 5 weeks.
- **India VIX** (the "fear gauge": how big a move traders expect) is 17.3. That is normal, but it rose 7.5% on Friday, which is a small warning sign.
- **This week:**
  - **Mon 23 Nov: monthly F&O expiry.** This is the last day of this month's futures and options contracts, which are bets on prices. Prices can swing more near 3:30 PM.
  - **Tue 24 Nov: market closed** for Guru Nanak Jayanti.
  - Thu 26 Nov: BSE's monthly expiry.
  - No NIFTY 50 company has results due this week.
- **FII/DII** (foreign big investors / Indian big investors such as mutual funds), from news sites quoting NSE's early figures:
  - On Fri 20 Nov, FIIs bought about ₹10,308 crore more than they sold, and DIIs sold about ₹4,860 crore more than they bought.
  - In November so far, FIIs have bought about ₹1.12 lakh crore net.
  - Sources: QuantsApp, Trendlyne, StockPil.
- **FII futures positions** (NSE file, 20 Nov): only 34% of FIIs' index futures are bets on a rise. They also hold a lot of "put" options, which are insurance against a fall. In words: they are buying shares but keeping protection.
- **Do conditions favour breakouts?** A breakout is a stock rising above a price ceiling it couldn't cross for weeks. **Mostly yes, with care.** The trend is up and foreign money is coming in. But expiry day, the Tuesday holiday and the rising VIX can make prices jumpy.

**Ideas** (scanned all 50 NIFTY stocks from NSE's official list)
- Axis Bank had the strongest day (+4.7% on 3.3× normal volume). But it is already 11.8% above its breakout price, so it is too late to buy safely.
- M&M and Hindustan Unilever: their longer trends are not up, so skip.
- ICICI Bank: strong, but it has no resting pattern to plan from yet.
- **Bajaj Finance is the only stock with a usable plan.**

| Stock | Suggestion | Reason | Entry (buy only if price rises to it) | Stop | Target | Risk-reward before / after charges | P(target) | Likely to hit target? |
|---|---|---|---|---|---|---|---|---|
| BAJFINANCE | **Buy (paper only)** | Has rested under ₹1,126.90 for about 15 weeks with smaller and smaller dips. But it has lagged NIFTY over 3 months (trend check 5 of 6). | ₹1,129.20 (skip if it opens above ₹1,163.08) | ₹1,068.60 | ₹1,250.40 | 2.0 : 1 / 1.64 : 1 | 16–21% | **No** |

*In words: we buy only if Bajaj Finance rises to ₹1,129.20, about 0.6% above Friday's close of ₹1,122.*
- If it then falls to ₹1,068.60, we sell and take the loss.
- If it rises to ₹1,250.40, we sell and take the profit.
- If it opens above ₹1,163.08 (more than 3% above our price), we don't buy at all.

**₹10,000 simulation (Groww rates as of 2026-10-31)**

| Qty | Invested | Charges (round trip) | Charges % | Net loss if stop hit | Net gain if target hit |
|---|---|---|---|---|---|
| 8 | ₹9,033.60 | ≈ ₹64–67 | 0.71% (no warning) | −₹548.74 | +₹902.43 |

*In words: we risk about ₹549 to try to make about ₹902. Charges take less than 1% of the money.*

**Honest caveat: the chance of reaching the target (P(target))**
- Method: backtest-lab, "buy when price breaks a 20-day high; stop 2×ATR; target 2R; sell after 20 days if neither is hit; ₹10,000 per trade; Groww charges". It used only data up to Fri 20 Nov.
- **All 50 NIFTY stocks over two years:** the target was hit first in only 83 of 525 trades (16%).
  - 154 trades ran out of time.
  - On average each trade lost ₹123 after charges.
- **Bajaj Finance alone:** 3 of 14 trades (21%).
- breakout-planner itself rated this stock "watch", not "buy".
- So this is a low-odds idea. We are logging it to learn, not because it looks strong.
