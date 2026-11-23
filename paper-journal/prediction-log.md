# Prediction log

> **SIMULATION ONLY: no real orders. Prices from delayed Yahoo Finance.**

Each morning we write down what we **expect** each idea to do. Each evening we write down what **actually** happened, and compare the two. Most differences will just be normal market ups and downs. One day proves nothing, in the same way that one bad month doesn't make a fund bad.

Cause codes (exactly one per difference):

| Code | Meaning |
|---|---|
| **a** | Normal market noise: the rules were followed, and this was just one of the possible outcomes |
| **b** | A gap at the open (an overnight jump) skipped our buy price or our stop |
| **c** | Data issue: delayed or missing prices |
| **d** | Cost issue: charges or slippage were larger than assumed |
| **e** | Rule or skill error: the setup logic, stop size, filter or sizing behaved wrongly |
| **f** | News or event surprise the tools could not have known |

Only **c, d and e** count as errors.

| Date | Stock | Setup reason | Pred entry | Pred stop | Pred target | Pred net loss at stop ₹ | Pred net gain at target ₹ | Pred charges ₹ | P(target) % | Likely to hit target? | Actual fill | Day high | Day low | Close | Stop/target hit? | Actual net P&L ₹ | Entry gap ₹ (%) | Outcome gap ₹ (%) | Cause | Error? | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | BAJFINANCE | 15-week base under ₹1,126.90, shrinking dips (grade B); trend 5/6 | 1,129.20 | 1,068.60 | 1,250.40 | −548.74 | +902.43 | 63.94 / 67.17 | 16 (83/525 NIFTY 50); 21 (3/14 stock) | No | 1,129.20 (open 1,125.25 was below the buy price) | 1,130.50 | 1,093.10 | 1,095.50 | Neither (OPEN, day 1 of 20) | −334.02 (unrealised, not final) | 0.00 (0%) | −334.02 vs ₹0 (−3.7%), not final | a | No | NIFTY −1.75% same day on monthly expiry; VIX 17.32→17.70; no company news found; rules followed |
