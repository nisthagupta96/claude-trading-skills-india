# Paper-trading journal

> **SIMULATION ONLY: no real orders. Prices are from delayed Yahoo Finance.**
> This is a pretend notebook. Nothing is bought or sold with real money.

Starting date: 2026-11-23

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

*In words: one pretend trade is planned and nothing has been bought yet. It becomes a real (pretend) purchase only if Bajaj Finance rises to ₹1,129.20 today.*

## Cumulative net P&L since start
Realised: ₹0.00 · Unrealised: ₹0.00

## Lessons covered

## Daily log

### 2026-11-23 Morning

**Market view** (data to Friday 20 Nov close)
- **Trend: "confirmed uptrend".** This is the trend tool's label for "the NIFTY 50 is clearly rising; a normal time to buy". NIFTY 50 is the index of India's 50 biggest companies, the one a Nifty index fund copies.
  - It closed at 25,801, 2.2% below its high for the year.
  - There have been 0 heavy-selling days in 5 weeks.
- **India VIX** (the "fear gauge": how big a move traders expect) is 17.3. That is normal, but it rose 7.5% on Friday.
- **GIFT Nifty** (an early-morning price that hints at how NIFTY may open) **could not be found for this morning.**
- **FII/DII** (foreign big investors / Indian big investors such as mutual funds):
  - On Fri 20 Nov, FIIs bought about ₹10,308 crore more than they sold, and DIIs sold about ₹4,860 crore net. These are NSE's early figures as quoted by QuantsApp, Trendlyne and StockPil.
  - In futures, only 34% of FIIs' index bets are on a rise, and they hold put options (insurance against a fall). They are buying shares but keeping protection.
- **This week:**
  - **Today: monthly F&O expiry**, the last day of this month's futures and options contracts (bets on prices). Prices can swing near 3:30 PM.
  - **Tue 24 Nov: market closed** for Guru Nanak Jayanti.
  - Thu 26 Nov: BSE monthly expiry.
  - No RBI or big data releases are listed. No NIFTY 50 results: the July–September results season ended on 14 Nov.
- **Favour breakouts?** A breakout is a stock rising above a price ceiling it couldn't cross for weeks. **Mostly yes, with care.** The trend is up and foreign money is coming in. But expiry day, tomorrow's holiday and a rising VIX can make moves jumpy.

**Ideas** (all 50 NIFTY stocks, NSE's official list)
- **Axis Bank:** best day on Friday (+4.7%), but already 11.8% above its breakout price. Too late to buy safely.
- **M&M and Hindustan Unilever:** their longer trends are not up.
- **ICICI Bank:** strong, but no resting pattern to plan from yet.
- **Bajaj Finance is the only usable setup.**

| Stock | Suggestion | Reason | Entry (buy only if price rises to it) | Stop | Target | Risk-reward before / after charges | P(target) | Likely to hit target? |
|---|---|---|---|---|---|---|---|---|
| BAJFINANCE | **Buy (paper only)** | Rested under ₹1,126.90 for about 15 weeks with smaller and smaller dips; but lagging NIFTY over 3 months (trend check 5 of 6) | ₹1,129.20 (skip if it opens above ₹1,163.08) | ₹1,068.60 | ₹1,250.40 | 2.0 : 1 / 1.64 : 1 | 16% (all NIFTY 50); 21% (this stock) | **No** |

*In words: we buy 8 shares only if Bajaj Finance rises to ₹1,129.20, about 0.6% above Friday's close of ₹1,122.*
- Then we sell at ₹1,068.60 if it falls, or at ₹1,250.40 if it rises.
- If it opens above ₹1,163.08 (more than 3% higher), we don't buy.
- Its last results came out on 19 Oct, so none are due this week.

**₹10,000 simulation (Groww rates as of 2026-10-31)**

| Qty | Invested | Charges (round trip) | Charges % | Net loss if stop hit | Net gain if target hit |
|---|---|---|---|---|---|
| 8 | ₹9,033.60 | ₹63.94 (stop) / ₹67.17 (target) | 0.71% (no warning) | −₹548.74 | +₹902.43 |

*In words: we risk about ₹549 to try to make about ₹902. Charges are under 1% of the money.*

**How P(target) was worked out:** backtest-lab, using "buy when price breaks a 20-day high; stop 2×ATR; target 2R; sell after 20 days if neither is hit; ₹10,000 per trade; Groww charges". It used only data up to Fri 20 Nov.
- **All 50 NIFTY stocks over two years:** the target was hit first in 83 of 525 trades (16%), and 154 trades ran out of time. The average result was −₹123 per trade after charges.
- **Bajaj Finance alone:** 3 of 14 trades (21%).
- breakout-planner rated it "watch", not "buy".
- This is a low-odds idea, logged to learn from.
