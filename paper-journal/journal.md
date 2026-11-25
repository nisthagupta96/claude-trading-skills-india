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
| 2026-11-23 | BAJFINANCE | OPEN | 1,129.20 | 1,068.60 | 1,250.40 | 8 | 9,033.60 | 30.30 |

*In words: we hold 8 pretend Bajaj Finance shares, bought at ₹1,129.20 on 23 Nov. After 25 Nov, this is day 2 of 20. We sell if the price closes at ₹1,068.60 or below, or at ₹1,250.40 or above.*

## Cumulative net P&L since start
Realised: ₹0.00 (no trade closed yet) · Unrealised: −₹47.86 (Bajaj Finance, if sold at the 25 Nov close, after charges)

## Lessons covered
- 2026-11-23: Stop-loss
- 2026-11-25: Target

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

### 2026-11-23 Close

> Run at 3:55 PM IST, earlier than the usual 4:35 PM, because the owner asked. The Yahoo prices may differ slightly from NSE's official close. The 4:35 PM run re-checks them.
>
> **4:35 PM check: confirmed.** NSE's official end-of-day file (bhavcopy) shows Bajaj Finance open ₹1,125.25, high ₹1,130.50, low ₹1,093.10 and close ₹1,095.50. These match the figures below exactly, so nothing changed.

**What happened today, in plain words**
- Bajaj Finance opened at ₹1,125.25, just below our ₹1,129.20 buy price.
- It rose to ₹1,130.50 during the day, so our pretend buy happened at ₹1,129.20.
- Then the whole market turned down. NIFTY opened higher, at 25,929, but closed at 25,350, down 1.75% on the day. Today was monthly expiry day, when big traders close their futures and options bets.
- Bajaj Finance closed at ₹1,095.50. That is ₹33.70 (3.0%) below what we paid, and still ₹26.90 (2.5%) above our sell-if-it-falls price of ₹1,068.60.

| Stock | Status | Day | Qty | Entry | Invested ₹ | Current price | Current value ₹ | Gross P&L ₹ | Gross P&L % | Charges ₹ | Net P&L ₹ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BAJFINANCE | OPEN | 1 of 20 | 8 | 1,129.20 | 9,033.60 | 1,095.50 | 8,764.00 | −269.60 | −2.98% | 64.42 | −334.02 |

*In words: our pretend shares are worth ₹8,764, against ₹9,034 paid. If we sold now, we'd lose ₹270 on the price plus ₹64 in charges, so ₹334 in total. We are not selling: neither the loss point nor the target was reached.*

- End-of-day net P&L (all stocks): **−₹334.02** (not yet realised: the trade is still open)
- Cumulative net P&L since start (2026-11-23): **₹0.00 realised**; −₹334.02 unrealised
- Free slots for tomorrow's trading day (Wed 25 Nov, since Tue is a holiday): **2 of 3**
- For comparison: a NIFTY index fund (NIFTYBEES) fell 1.63% today. Our stock fell 3.0% from our buy price.

#### Prediction vs reality

**The story:** we planned to buy Bajaj Finance only if it rose to ₹1,129.20. It did, briefly, reaching ₹1,130.50. Then the whole market fell, and the stock ended the day 3% lower. Nothing went wrong with the rules. We bought on a day the market reversed.

| | Predicted | Actual | Gap |
|---|---|---|---|
| Buy price | ₹1,129.20 | ₹1,129.20 (the open was ₹1,125.25, below it, so no gap) | ₹0 (0%) |
| Day range | — | High ₹1,130.50, low ₹1,093.10 | — |
| Stop ₹1,068.60 / target ₹1,250.40 | — | Neither touched (the low stayed ₹24.50 above the stop) | — |
| Close | — | ₹1,095.50 | −2.98% vs the buy price |
| Net result | −₹548.74 at stop / +₹902.43 at target | −₹334.02 if sold now (not final; the trade is still open) | vs ₹0: −₹334.02 (−3.7% of the money in) |
| Charges | ₹63.94 (at stop) | ₹64.42 (if sold today) | +₹0.48 |

**Cause: (a) normal market noise. Not an error.**
- The rules were followed exactly: the buy happened only once the price reached ₹1,129.20, the quantity was 8, the stop is 2×ATR and the target is 2R.
- Evidence: NIFTY fell 1.75% on the same day (25,800.60 → 25,349.65), so the whole market dropped, not just this stock. India VIX rose to 17.70. Today was monthly expiry. No Bajaj Finance news was found.
- In plain words: it's like starting a SIP on a day the whole market falls. Bad timing, but not a broken plan. The odds we wrote this morning already said most trades like this don't reach the target.

**Repeat-cause check:** data issues 0, cost issues 0, rule/skill errors 0 (the threshold is 5 trades or 4 weeks). **No change needed, this is expected variation.**

#### Today's lesson in plain words

**(1) How to read today's table**
- *Stock*: the company's short name on the stock exchange (BAJFINANCE = Bajaj Finance).
- *Status*: OPEN means we still hold the shares.
- *Day*: how many trading days we have held it. After 20, we sell whatever happens.
- *Qty*: the number of shares. Only whole shares are possible, unlike fund units.
- *Entry*: the price we paid per share.
- *Invested ₹*: the money put in (8 × ₹1,129.20).
- *Current price*: today's closing price. A share price moves all day, while a fund's NAV is set once a day.
- *Current value ₹*: what our 8 shares are worth now.
- *Gross P&L*: profit or loss before costs, in ₹ and %.
- *Charges ₹*: the cost of buying and selling (brokerage, taxes, fees), like a fund's expense ratio plus exit load.
- *Net P&L ₹*: what you would really gain or lose after charges.

**How did today go?** Badly on paper, about −₹334. The plan worked as designed. The market as a whole fell almost 2% the same afternoon, and our stock fell with it.

**(2) What could we have done better today?**
- **Honest point:** the buy happened on monthly expiry day, the day before a holiday, with the fear gauge rising. The morning report flagged all three as reasons for "care", but our rules don't stop a buy on such days. One bad day doesn't prove they should, so we keep the rules. It's worth watching whether breakouts bought on expiry days fail more often.
- **For tomorrow:** nothing to change. The stock is still 2.5% above our sell point. The plan says hold, so we hold. Selling now out of worry would be breaking our own rule.

**(3) Today's metric lesson: Stop-loss**
- *What it is:* a price, decided before buying, at which you sell if the trade goes wrong. Ours is ₹1,068.60.
- *Mutual-fund comparison:* most fund investors never set one, because a diversified fund rarely falls hard and they hold for years. A single stock can fall 10–20% on one piece of news, so a trader decides the exit in advance, while calm.
- *Why it matters:* it caps the damage. We know the worst normal-case loss on this trade is about ₹549. Without a stop, a small loss can grow while you "wait to get back to what you paid".
- *How to read it:* our stop sits two "normal days' movement" (2 × ATR, about ₹30 each) below the buy price. Today was a fairly bad day, and the stock fell ₹37 from its high, but it is still ₹26.90 above the stop. That is the point of the 2×ATR distance: it leaves room for ordinary bad days.
- *Example from today:* had we used a tighter stop of 1 × ATR (₹1,098.90), we would have been sold today at a loss, at almost the lowest point of the day. The 2×ATR stop kept us in.
- *A catch:* our simulation checks the stop against the **closing** price. In real trading, a stop order fires the moment the price touches it during the day, and after bad overnight news it can fill well below the stop.

**(4) Question for tonight**
If Bajaj Finance falls another 2% on Wednesday but stays above ₹1,068.60, would you feel the urge to sell, and what would following the rule teach you either way?

### 2026-11-24 Morning
Market holiday (Guru Nanak Jayanti / Prakash Gurpurb): NSE and BSE are closed, so there are no ideas today. Bajaj Finance stays open with nothing changed. Holidays do not count towards the 20-day limit. Next trading day: Wed 25 Nov.

### 2026-11-24 Close
Market holiday (Guru Nanak Jayanti / Prakash Gurpurb). Positions unchanged: Bajaj Finance is still OPEN at day 1 of 20, last priced at ₹1,095.50 (Monday close). There is no lesson and no comparison today.

### 2026-11-25 Morning

**Market view** (data to Mon 23 Nov close; Tuesday was a holiday)
- **Trend: still "confirmed uptrend"** (the trend tool's label for "a normal time to buy"). The risk score rose from 3 to 8 out of 100.
  - NIFTY closed Monday at 25,350, 3.9% below its yearly high. That is a small pullback (a short dip within an uptrend).
  - Monday's 1.75% fall came on lower volume than Friday, so the tool did not count it as a heavy-selling day. There have been 0 such days in 5 weeks.
- **India VIX** (the "fear gauge") is 17.7: normal, but rising.
- **GIFT Nifty for this morning was not found.** On Monday, reports mentioned a sell-off in US technology shares.
- **FII/DII** (foreign / Indian big investors) on Mon 23 Nov:
  - FIIs bought ₹5,673 crore net, and DIIs sold ₹2,760 crore net (NSE provisional figures, via Finostat, Tapetide and NiftyTrader).
  - **Big change in futures:** only **20.1%** of FIIs' index futures bets are now on a rise, down from 34.1% on Friday. That is at the "extreme caution" level. They are buying shares in cash but have cut their futures bets on a rise sharply. That is a mixed signal.
- **This week:** Thu 26 Nov: BSE monthly expiry (SENSEX). No RBI or big data releases. No NIFTY 50 results due.
- **Favour breakouts? Mixed.** The trend is still up. But the market fell on Monday, the fear gauge is rising, and foreign investors are very cautious in futures.

**Ideas: no good setup today.** We already hold Bajaj Finance, so 2 places are free, but nothing qualifies:
- Apollo Hospitals is 6.5% above its breakout price, and Axis Bank is 7.3% above its own. Both are too late to buy safely.
- Cipla, M&M and Shriram Finance are near their breakout prices but fail most trend checks (2 or fewer out of 6).
- ICICI Bank is strong but has no resting pattern yet.
- Bajaj-Auto is above ₹10,000 per share.

*In words: sitting out is also a decision. With no clean setup and mixed signals, we buy nothing new today.*

**Open trade:** Bajaj Finance, held since 23 Nov (day 2 of 20 today). Last price ₹1,095.50; stop ₹1,068.60; target ₹1,250.40.

### 2026-11-25 Close

**What happened today, in plain words**
- The whole market bounced back. NIFTY rose 1.85% (25,350 → 25,819), recovering most of Monday's fall.
- Bajaj Finance opened at ₹1,119.90, a jump of 2.2% above Monday's close. It went as high as ₹1,148, then closed at ₹1,131.35, up 3.3% on the day.
- That is ₹2.15 above what we paid. But after charges, selling now would still lose a little, because we need ₹1,137.35 just to cover costs.
- No new idea was planned this morning, so there was no new buy.

| Stock | Status | Day | Qty | Entry | Invested ₹ | Current price | Current value ₹ | Gross P&L ₹ | Gross P&L % | Charges ₹ | Net P&L ₹ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BAJFINANCE | OPEN | 2 of 20 | 8 | 1,129.20 | 9,033.60 | 1,131.35 | 9,050.80 | +17.20 | +0.19% | 65.06 | −47.86 |

*In words: our pretend shares are worth ₹17 more than we paid. Selling costs about ₹65, so if we sold now we would be ₹48 down overall. We hold: the stop (₹1,068.60) and the target (₹1,250.40) were both far away today.*

- End-of-day net P&L (all stocks): **−₹47.86**, unrealised (better by ₹286 than Monday's −₹334.02)
- Cumulative net P&L since start (2026-11-23): **₹0.00 realised**; −₹47.86 unrealised
- Free slots for tomorrow: **2 of 3**
- For comparison: a NIFTY index fund (NIFTYBEES) rose 1.6% today.
- Data note: NSE's official end-of-day file was not out yet at 4:35 PM (error 404), so these are Yahoo prices.

#### Prediction vs reality

**The story:** no new idea today. Our one open trade, Bajaj Finance, recovered with the market. It is back above our buy price before charges, and still well between the stop and the target.

| | Predicted | Actual so far (day 2) | Gap |
|---|---|---|---|
| Stop ₹1,068.60 / target ₹1,250.40 | One of them to be hit within 20 days | Neither touched today (low ₹1,112.30, high ₹1,148.00) | — |
| Close | — | ₹1,131.35 (+0.19% vs the buy price) | — |
| Net result | −₹548.74 at stop / +₹902.43 at target | −₹47.86 if sold now (not final) | vs ₹0: −₹47.86 (−0.5%) |

**Cause: (a) normal market noise.** The stock moved with the market: NIFTY +1.85%, Bajaj Finance +3.3%. The rules were followed. Nothing is final while the trade is open.

**Repeat-cause check:** data issues 0, cost issues 0, rule/skill errors 0 (threshold: 5 trades or 4 weeks). **No change needed, this is expected variation.**

#### Today's lesson in plain words

**(1) How to read today's table**
- *Status OPEN*: we still hold the shares.
- *Day 2 of 20*: the second trading day since buying. The holiday doesn't count.
- *Current price / value*: today's closing price, and what our 8 shares are worth at it.
- *Gross P&L*: the gain before costs: +₹17.20, or +0.19%.
- *Charges*: the cost of buying and selling: ₹65.06.
- *Net P&L*: what is left after costs: −₹47.86.

**How did today go?** Well. The market recovered and our loss on paper shrank from ₹334 to ₹48. It shows how much a single stock can swing in two days, much more than a fund's NAV usually does.

**(2) What could we have done better today?**
- **Nothing to change.** On Monday, at −₹334, it was tempting to sell. Holding was the rule, and today shows why: normal swings go both ways. One good day doesn't prove the rule is right either, but it shows why we decide exits in advance and not on feelings.
- **Something to notice:** the price is ₹2 above our buy price, yet we are still at a loss. That's the charges. A trade has to rise about 0.7% (to ₹1,137.35) just to break even.

**(3) Today's metric lesson: Target**
- *What it is:* a price, decided before buying, at which we sell to take the profit. Ours is ₹1,250.40.
- *How ours is set:* it is 2 × the risk above the buy price. The risk is the distance to the stop: ₹1,129.20 − ₹1,068.60 = ₹60.60 per share. So the target is ₹1,129.20 + 2 × ₹60.60 = ₹1,250.40.
- *Why it matters:* without a target, people often sell winners too early (out of fear of losing the gain) or hold too long (hoping for more). A fixed target makes the plan automatic. It also lets us measure how often the plan works.
- *Mutual-fund comparison:* it's like deciding "I'll redeem when this fund is up 10%" instead of checking the NAV every day and deciding by mood.
- *How to read it:* at today's close (₹1,131.35), the target is ₹119.05 away (+10.5%), and the stop is ₹62.75 away (−5.5%). So the stock needs to rise about twice as far to hit the target as it would need to fall to hit the stop. That's by design: we accept that we will be right less often, but win twice as much when we are.
- *The honest part:* past data said only about 1 in 6 trades like this reached the target within 20 days. The target is a plan, not a promise.

**(4) Question for tonight**
If Bajaj Finance rises to ₹1,200 but then starts falling, would you be tempted to sell before the target? What would the rule say?
