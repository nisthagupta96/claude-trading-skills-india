# Paper-trading journal: DRY RUN (replay of Friday 20 Nov 2026)

> **SIMULATION ONLY: no real orders. Prices from delayed Yahoo Finance.**
> This is a one-off test, run on Sunday 22 Nov 2026. The "morning" step used only data up to Thursday 19 Nov's close
> (files cut off at that date, and every script run with `--as-of 2026-11-19` or the truncated files).
> The "closing" step then revealed Friday 20 Nov's prices. The real journal (`paper-journal/`) starts fresh on Monday 23 Nov.

Starting date: 2026-11-20 (test)

## Open positions

| Date | Stock | Status | Entry | Stop | Target | Qty | Invested ₹ | ATR |
|---|---|---|---|---|---|---|---|---|
| 2026-11-20 | BAJFINANCE | NOT TRIGGERED | 1,129.20 | 1,071.10 | 1,245.40 | 1 | 1,129.20 | 29.05 |

## Cumulative net P&L since start
Realised: ₹0.00 · Unrealised: ₹0.00

## Lessons covered
- 2026-11-20: Stop-loss

## Daily log

### 2026-11-20 Morning (as of 07:38 IST, data to Thu 19 Nov close)

**Market view**
- NIFTY 25,514 (Thu close). market-regime: **CONFIRMED UPTREND**, risk score 3/100, exposure ceiling 100%, max 5 new positions. 0 distribution days in 25 sessions. Follow-through day 15 Oct. NIFTY is 8.8% above its 50 DMA and 3.3% below its 52-week high.
- India VIX 16.1 (moderate). GIFT Nifty and global cues could not be reconstructed for a past morning.
- FII/DII flows: **not available.** The NSE website is blocked from this environment, so fii-dii-flows had no input file.
- Events: weekly SENSEX expiry Thu 19 Nov. Next week: NSE monthly expiry **Mon 23 Nov** (moved forward) and **market holiday Tue 24 Nov** (Guru Nanak Jayanti). No NIFTY 50 results due: the Q2 results deadline was 14 Nov.
- **Favour breakouts? Yes, on the market.** But the scan found almost no stock-level setups (see below).

**Scans** (NIFTY 50 list as known to Claude; NSE's official list could not be downloaded)
- momentum-scanner: INDIGO (episodic pivot), M&M (burst), HINDUNILVR (burst) are all above ₹2,000 and excluded. ICICIBANK is a strength leader with no base yet.
- breakout-planner: of the stocks under ₹2,000, only BAJFINANCE is rated "watch". The rest are "skip" (MAXHEALTH and SUNPHARMA fail 3 of 6 trend checks; ICICIBANK has no base).

**Ideas**

| Stock | Claude suggestion | Reason (one line) | Entry (buy-stop) | Stop (−2×ATR) | Target (2R) | Risk-reward (before / after charges) | P(target) |
|---|---|---|---|---|---|---|---|
| BAJFINANCE | **Skip** (logged as a shadow trade for this test) | B-grade VCP base, 3% below its ₹1,126.90 pivot, but trend template only 5/6 (lagging NIFTY over 3 months) | ₹1,129.20 | ₹1,071.10 | ₹1,245.40 | 2.0 : 1 / **0.8 : 1** | 29% |
| ICICIBANK | Skip | Strongest stock vs NIFTY, but no base yet (high only 6 days ago) | n/a | n/a | n/a | n/a | n/a |
| MAXHEALTH | Skip | A-grade base at its pivot, but downtrend structure (200 DMA falling, 3/6 trend checks) | n/a | n/a | n/a | n/a | n/a |

**Verdict: no good setup today.**

**₹2,000 simulation for BAJFINANCE (Groww rates as of 2026-10-31)**

| Qty | Invested | Charges (round trip) | Charges % of invested | Net loss if stop hit | Net gain if target hit |
|---|---|---|---|---|---|
| 1 | ₹1,129.20 | ₹37.85 (brokerage ₹10, STT ₹2.20, exchange ₹0.07, stamp ₹0.17, GST ₹1.81, DP ₹23.60) | **3.35% ⚠ WARNING: above 2%** | −₹95.95 | +₹78.17 |

P(target) method: backtest-lab `donchian-breakout` (20-day high breakout, 2×ATR stop, 2R target, ₹2,000 per trade, Groww charges) on all 50 stocks, 2 years to 19 Nov 2026 only. Target hit first in 92 of 318 trades = **29%**. Average net result: **−₹44.5 per trade**. Average charges were 2.5% of the amount invested. On BAJFINANCE alone: 5 of 14 hit target, and charges were 89% of gross profit.

### 2026-11-20 Close (Friday's prices revealed)

| Stock | Status | Qty | Entry | Invested ₹ | Current/Exit price | Current/Exit value ₹ | Gross P&L ₹ | Gross P&L % | Charges ₹ | Net P&L ₹ |
|---|---|---|---|---|---|---|---|---|---|---|
| BAJFINANCE | NOT TRIGGERED | 0 | (1,129.20) | 0.00 | 1,122.00 | 0.00 | 0.00 | 0.00% | 0.00 | 0.00 |

End-of-day net P&L (all stocks): **₹0.00**
Cumulative net P&L since start (2026-11-20): **₹0.00** realised, ₹0.00 unrealised.

Friday for reference: NIFTY +1.12% (25,514 → 25,801). BAJFINANCE high ₹1,125.00, close ₹1,122.00 (+2.7%). ICICIBANK +1.9%. MAXHEALTH opened +2.3% above its pivot and closed +3.9%.

#### Prediction vs reality

| | Predicted | Actual | Gap |
|---|---|---|---|
| Entry | Buy at ₹1,129.20 if the price got there | Day high ₹1,125.00, so **not filled** | Missed by ₹4.20 (0.37%) |
| Stop / target | Stop ₹1,071.10, target ₹1,245.40 | Neither touched (low ₹1,078.15, high ₹1,125.00) | n/a |
| Close | n/a | ₹1,122.00 | 0.6% below the buy price |
| Net P&L | −₹95.95 at stop, +₹78.17 at target | ₹0 (no trade) | Not final: no trade was opened |
| Charges | ₹37.85 | ₹0 | n/a |

**Cause: (a) normal market noise. Not an error.** The rule was "buy only if the price clears the pivot", and it didn't, by ₹4.20.
Evidence: Yahoo bar complete (Sunday download); the high of ₹1,125.00 is below the pivot of ₹1,126.90 itself, so the buffer did not cause the miss; no news and no gap.

In plain words: we set a "buy only if it reaches ₹1,129.20" instruction. It's like saying "I'll start a SIP in this fund only if its NAV crosses 50". The price came very close but never got there, so nothing was bought and nothing was lost. That is the rule working, not failing.

What a skipped stock did: MAXHEALTH, which we skipped because its longer trend is still down, jumped 3.9%. One day of a skipped stock rising is not evidence that the filter is wrong, in the same way that one good month doesn't make a fund good. It is logged in the prediction log so a pattern can show up over time.

**Repeat-cause check:** errors so far: data 0, cost 0, rule/skill 0 (threshold: 5 trades or 4 weeks). **No change needed, this is expected variation.**

#### Today's lesson in plain words

**(1) How to read today's table**
- *Stock*: the company's short name on the NSE (National Stock Exchange). BAJFINANCE = Bajaj Finance.
- *Status*: what happened to our plan. "NOT TRIGGERED" means the price never reached our buy level, so we never bought.
- *Qty*: how many shares we own. Shares come whole. A fund gives you 3.217 units; a stock only gives 1, 2 or 3 shares.
- *Entry*: the price we planned to buy at.
- *Invested ₹*: money actually put in (Qty × Entry). Here ₹0, because nothing was bought.
- *Current/Exit price*: a stock's price changes every second from 9:15 AM to 3:30 PM. A fund's NAV is set only once a day. This column shows the last price of the day.
- *Current/Exit value ₹*: what our shares are worth now (Qty × current price).
- *Gross P&L ₹ / %*: profit or loss before costs, in rupees and as a percentage.
- *Charges ₹*: costs of buying and selling (brokerage, taxes, fees). They are like a fund's expense ratio and exit load, but you pay them on every trade.
- *Net P&L ₹*: what is really left in your pocket after charges.

How did today go? **Neutral.** We bought nothing, so we made nothing and lost nothing. The market rose 1.1%, so a NIFTY index fund would have made about ₹14 on ₹1,129. Sitting out cost a little in opportunity but nothing in money.

**(2) What could we have done better today**
- **The bigger finding is in the morning numbers, not the outcome.** With ₹2,000 per stock, one share of Bajaj Finance costs ₹37.85 to buy and sell. That is 3.4% of the money, mostly the fixed ₹23.60 DP charge on selling. It turns a 2-to-1 bet into a 0.8-to-1 bet after charges. Over the last two years this exact rule lost about ₹44 per trade on NIFTY 50 stocks.
- **Change for tomorrow:** keep following the rules, but read "Net gain if target hit" before "Gain". If the net risk-reward is below 1.5 to 1, treat the idea as Skip. (This is a reading habit, not a rule change. Any rule change has to go through the proposal process.)

**(3) Today's metric lesson: Stop-loss**
- *What it is:* a price, decided before you buy, at which you will sell if the trade goes wrong. It caps how much one bad trade can hurt.
- *Mutual-fund comparison:* imagine telling yourself "if this fund falls 5% from what I paid, I redeem". Most fund investors never do this, because funds are diversified and meant for years. A single stock can fall 20% in a day on bad news, so a trader needs the exit decided in advance, while calm.
- *Why it matters:* without a stop, a small loss can grow into a big one, and you start "waiting to get back to break-even". With one, you know your worst case before you start.
- *How to read it:* our stop is "entry − 2 × ATR". ATR is the stock's usual daily move (more on this in a later lesson). For Bajaj Finance, ATR ≈ ₹29, so the stop sits ₹58.10 (5.1%) below the ₹1,129.20 entry, at ₹1,071.10. Too tight, and normal daily wobbles knock you out. Too loose, and each loss is big.
- *Real example from today:* Friday's low for Bajaj Finance was ₹1,078.15, only ₹7 above our ₹1,071.10 stop. If we had been holding the stock, it would have survived, just. A stop at 1×ATR (₹1,100) would have been hit. This is why the rules use 2×ATR.
- *A catch:* a stop order is not a guarantee. If a stock opens far below the stop after bad overnight news (a "gap-down"), you sell at the open, which can be much lower. The backtest found 40 of 318 trades hit the stop this way.

**(4) Question for tonight**
If the costs of a trade are 3.4% and the target is 10% away, how much of the possible gain would you really keep, and would you still take the trade?

### Week ending 2026-11-20: Review (dry run, one day only)
- Ideas: 1 shadow idea (BAJFINANCE, not triggered). Trades: 0. Wins 0, losses 0. Charges ₹0. Net ₹0.
- Same ₹1,129.20 for 1 day: bank FD at 7% a year ≈ +₹0.22. NIFTY 50 index fund (NIFTYBEES +1.24%, minus about 0.04% a year expense ratio) ≈ +₹14.
- Calibration: 0 closed trades, so nothing to measure yet. About 30 or more closed trades are needed before "expected 29% vs actual X%" means anything.
- Causes: 1 × (a) noise. Errors 0. No change needed.
- Worth following? Not enough data. The warning sign is structural, not from this day: at ₹2,000 per stock, charges of about 2.5–3.5% wipe out much of the edge of a 2R breakout.
