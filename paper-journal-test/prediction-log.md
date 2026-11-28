# Prediction log: DRY RUN (replay of Friday 20 Nov 2026)

> SIMULATION ONLY: no real orders. Prices from delayed Yahoo Finance.

This file compares what the morning plan **predicted** with what **actually happened**. Think of it as checking a fund's "expected return" against what it really delivered, trade by trade. Most gaps will be normal market noise. One day proves nothing.

Cause codes:
- **a** = normal market noise
- **b** = a gap at the open skipped the entry or stop
- **c** = data issue
- **d** = cost issue
- **e** = rule or skill error
- **f** = news or event surprise

Only **c, d and e** count as errors.

| Date | Stock | Setup reason | Pred entry | Pred stop | Pred target | Pred net loss at stop ₹ | Pred net gain at target ₹ | Pred charges ₹ | P(target) % | Likely to hit target? | Actual fill | Day high | Day low | Close | Stop/target hit? | Actual net P&L ₹ | Entry gap ₹ (%) | Outcome gap ₹ (%) | Cause | Error? | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-20 | BAJFINANCE (shadow; suggestion was Skip) | VCP base B, 3% below pivot ₹1,126.90, trend 5/6 | 1,129.20 | 1,071.10 | 1,245.40 | −95.95 | +78.17 | 37.85 | 29 | No | Not filled | 1,125.00 | 1,078.15 | 1,122.00 | Neither | 0.00 | −4.20 (−0.37%) short of trigger | n/a (no trade) | a | No | High ₹1,125.00 < pivot ₹1,126.90; complete Yahoo bar; no gap; no news |
