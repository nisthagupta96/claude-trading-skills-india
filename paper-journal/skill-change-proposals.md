# Rule-change proposals

> SIMULATION ONLY. A change is proposed only with evidence tested on past data that was not used to design it. Nothing changes until the owner approves.

## Proposal 1 (2026-11-28): wider stop, longer hold, market-trend filter. Status: AWAITING OWNER APPROVAL

**Problem.** The owner asked why the current rules rarely make money. On 10 years of NIFTY 50 data, the current rules made a small profit in 2016–2021 (+₹21 per trade) but lost in 2022–2026 (−₹54 per trade).
- 1,317 of 3,144 trades hit the stop. The stop sits just 2 normal days' movement below the buy price, so ordinary wobbles knock trades out.
- 1,012 trades hit the 20-day time limit, averaging only +₹161. The time limit sells many trades before they can work.
- Result: the average win (₹553) is barely bigger than the average loss (₹455), instead of about 2× as planned. With charges of about ₹65 per trade, that loses money.

**Method.** backtest-lab, all current NIFTY 50 stocks, ₹10,000 per trade, Groww charges, signal on the close and buy at the next open.
- Variations were judged separately on **2016-12 to 2021-12** and **2022-01 to 2026-11**. A change counts only if it helps in both periods.
- Nearby settings were also tested, to check the result holds when the numbers are nudged (a "plateau", not a lucky "spike").

**Average net result per trade after charges**

| Rules | Trades 2016–21 / 2022–26 | Win % 2016–21 / 2022–26 | ₹ per trade 2016–21 | ₹ per trade 2022–26 |
|---|---|---|---|---|
| **Current**: stop 2×ATR, target 2R, max 20 days | 1,578 / 1,566 | 45% / 40% | +21 | **−54** |
| Current + only buy when NIFTY is above its 200-day average | 1,212 / 1,261 | 44% / 40% | +14 | −55 |
| **A**: stop 3×ATR, target 3R, max 60 days, NIFTY filter | 699 / 758 | 44% / 39% | +227 | **+63** |
| A, stop 3.5×ATR, target 3R, 60 days | 638 / 698 | 48% / 43% | +265 | +90 |
| A, stop 3×ATR, target 4R, 60 days | 651 / 720 | 44% / 39% | +251 | +75 |
| A, stop 2.5×ATR, target 3R, 60 days | 770 / 837 | 42% / 35% | +201 | +19 |
| **B**: buy a new 52-week high; sell on a close below the 50-day average; stop 2.5×ATR; NIFTY filter | 255 / 296 | 35% / 29% | +223 | **+168** |
| B with stop 3×ATR | 239 / 285 | 38% / 31% | +291 | +185 |
| B, exit on the 100-day average, stop 3×ATR | 192 / 217 | 32% / 30% | +392 | +522 |
| B, exit on the 20-day average | 367 / 435 | 35% / 27% | +63 | −32 |

*In words: the stop distance and the holding time matter most. Every version with a stop of 3× or more and a 60-day limit made money in both periods, and every version with a 2× stop and a 20-day limit lost in recent years. Version B ("buy stocks at new yearly highs and ride them until the trend breaks") was the steadiest in recent years.*

**Suggested change** (to the scheduled-task rules, not to any skill file), choose one:
- **A (smallest change):** stop = entry − 3×ATR; target = entry + 3×(entry − stop); max 60 trading days; new buys only when NIFTY closes above its 200-day average.
- **B (different style):** buy when a stock closes at a new 52-week high; sell on a close below its 50-day average or at a stop of entry − 3×ATR; no fixed target; new buys only when NIFTY is above its 200-day average.

**Risks and honest caveats**
- **Survivorship bias:** the test uses *today's* NIFTY 50 members, which are past winners. Real results would be worse than these numbers.
- **Curve-fitting:** the settings were chosen after seeing the 2016–21 period. The 2022–26 period is the fairer check, and the gains there are much smaller (+₹63 to +₹168 per trade, about 0.6–1.7% of ₹10,000).
- **Bigger losses per trade:** a 3×ATR stop means losing about 7–9% (₹700–₹900) when wrong, against about 5% now.
- **Fewer, longer trades:** holds average about 35 days, so with 3 places we'd make only about 20 trades a year. That is slow to judge.
- **May not beat an index fund:** about 20 trades × ₹63–₹168 is roughly ₹1,300–₹3,400 a year on up to ₹30,000. That is about 4–11%, similar to or below a NIFTY index fund's long-run average, with more effort and risk.
- **Mid-trial change:** switching now makes week 1 not comparable with later weeks. Only one trade has been taken so far, so the cost is small.

**Status: AWAITING OWNER APPROVAL.** If approved, only the scheduled-task rules change (no skill files). The current Bajaj Finance trade keeps its original rules until it closes.
