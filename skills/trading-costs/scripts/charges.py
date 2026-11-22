#!/usr/bin/env python3
"""Trading-charges calculator for Indian equity and equity-derivative trades (NSE/BSE).

Zero dependencies (Python 3.10+ stdlib only).

Examples
--------
  # Delivery trade on Zerodha: buy 100 @ 1800, sell @ 1900
  python3 charges.py --segment delivery --buy 1800 --sell 1900 --qty 100 --broker zerodha

  # Compare every broker for an intraday trade
  python3 charges.py --segment intraday --buy 2450 --sell 2465 --qty 200 --broker all

  # NIFTY options: 2 lots (65 qty each) bought @ 120, sold @ 150
  python3 charges.py --segment options --buy 120 --sell 150 --qty 130 --broker groww

  # Delivery bought with MTF, held 20 days, ₹1,00,000 funded by broker
  python3 charges.py --segment mtf --buy 500 --sell 540 --qty 400 --broker zerodha \
      --mtf-days 20 --mtf-funded 100000

  # JSON output for programmatic use
  python3 charges.py --segment futures --buy 25000 --sell 25100 --qty 65 --json

Rates are statutory/exchange rates plus each broker's published pricing as of
RATES_AS_OF. Brokers change pricing; pass --brokerage-pct/--brokerage-cap/--brokerage-flat
to override, and always confirm against your contract note.
"""
from __future__ import annotations

import argparse
import json
import sys

RATES_AS_OF = "2026-10-31"

SEGMENTS = ("delivery", "intraday", "futures", "options", "mtf")

# ---------------------------------------------------------------------------
# Statutory and exchange charges (fractions; options apply to PREMIUM turnover)
# ---------------------------------------------------------------------------
# Securities Transaction Tax. F&O rates raised by Finance Act 2026, effective 1 Apr 2026:
#   futures 0.02% -> 0.05% (sell), options 0.10% -> 0.15% of premium (sell).
STT = {
    "delivery": {"buy": 0.001, "sell": 0.001},
    "mtf": {"buy": 0.001, "sell": 0.001},
    "intraday": {"buy": 0.0, "sell": 0.00025},
    "futures": {"buy": 0.0, "sell": 0.0005},
    "options": {"buy": 0.0, "sell": 0.0015},
}
# Options bought and exercised: 0.15% of intrinsic value (settlement price x qty).
STT_OPTIONS_EXERCISE = 0.0015

# Exchange transaction charges (NSE revision effective 1 Mar 2026).
# BSE cash-segment rate shown is for A/B group scrips; other groups are higher.
EXCHANGE_TXN = {
    "NSE": {"delivery": 0.0000307, "mtf": 0.0000307, "intraday": 0.0000307,
            "futures": 0.0000183, "options": 0.0003553},
    "BSE": {"delivery": 0.0000375, "mtf": 0.0000375, "intraday": 0.0000375,
            "futures": 0.0, "options": 0.000325},
}
SEBI_FEE = 10 / 1e7          # ₹10 per crore of turnover
IPFT_NSE = 0.01 / 1e7        # ₹0.01 per crore (NSE Investor Protection Fund Trust)
GST = 0.18                   # on brokerage + exchange txn + SEBI fee + IPFT (+ DP charge)
# Stamp duty (buy side only), uniform nationwide since 1 Jul 2020.
STAMP = {"delivery": 0.00015, "mtf": 0.00015, "intraday": 0.00003,
         "futures": 0.00002, "options": 0.00003}
# Exchange cap on brokerage in the cash segment: 2.5% of contract value.
SEBI_BROKERAGE_CAP_CASH = 0.025

# ---------------------------------------------------------------------------
# Rate history: the statutory and exchange rates in force on a given date, for backtests
# that span years (calculate(..., on=date)). Each era changes only what it lists, from its
# start date on. Broker brokerage and DP charges are NOT dated: every era uses BROKERS below.
#   verified=True : taken from the Finance Act, a SEBI circular or the exchange's own notice
#   verified=False: a documented approximation; backtests print the note so the reader knows
# The last era must reproduce the current constants above (tests/test_charges.py checks it).
# ---------------------------------------------------------------------------
RATE_HISTORY_START = "2013-06-01"
_BASELINE = {   # from 1 Jun 2013 (Finance Act 2013 STT cuts)
    "STT": {"delivery": {"buy": 0.001, "sell": 0.001}, "mtf": {"buy": 0.001, "sell": 0.001},
            "intraday": {"buy": 0.0, "sell": 0.00025}, "futures": {"buy": 0.0, "sell": 0.0001},
            "options": {"buy": 0.0, "sell": 0.0005}},
    "EXCHANGE_TXN": {
        "NSE": {"delivery": 0.0000325, "mtf": 0.0000325, "intraday": 0.0000325,
                "futures": 0.000019, "options": 0.0005},
        "BSE": dict(EXCHANGE_TXN["BSE"]),
    },
    "SEBI_FEE": 15 / 1e7,
    "STAMP": {"delivery": 0.0001, "mtf": 0.0001, "intraday": 0.00002, "futures": 0.00002, "options": 0.00002},
    "GST": 0.1236,     # service tax 12% + 3% education cess
}
# Components of the baseline that are approximations, until an era replaces them.
_BASELINE_APPROX = {
    "EXCHANGE_TXN.NSE": "NSE charged turnover slabs before Oct 2024; the top-slab rate is used "
                        "(differences are under ₹0.25 per ₹1 lakh traded in cash).",
    "EXCHANGE_TXN.BSE": "BSE transaction charges use today's schedule for every year.",
    "STAMP": "Stamp duty before 1 Jul 2020 was set state by state; a typical Maharashtra rate is used "
             "(0.01% delivery buy, 0.002% intraday and F&O buy).",
    "SEBI_FEE": "SEBI turnover fee ₹15/crore before the 2020 cut to ₹10/crore.",
}
RATE_HISTORY = [
    {"from": "2015-06-01", "verified": True, "set": {"GST": 0.14}, "note": "Service tax 14%."},
    {"from": "2015-11-15", "verified": True, "set": {"GST": 0.145}, "note": "Service tax 14% + Swachh Bharat cess 0.5%."},
    {"from": "2016-06-01", "verified": True, "set": {"GST": 0.15}, "note": "Service tax 14% + SBC 0.5% + KKC 0.5%."},
    {"from": "2017-07-01", "verified": True, "set": {"GST": 0.18}, "note": "GST 18% replaces service tax."},
    {"from": "2020-06-01", "verified": False, "set": {"SEBI_FEE": 10 / 1e7},
     "note": "SEBI turnover fee ₹10/crore; the effective date of the cut from ₹15 is approximate."},
    {"from": "2020-07-01", "verified": True,
     "set": {"STAMP": {"delivery": 0.00015, "mtf": 0.00015, "intraday": 0.00003, "futures": 0.00002,
                       "options": 0.00003}},
     "note": "Uniform stamp duty under the amended Indian Stamp Act."},
    {"from": "2021-01-01", "verified": False,
     "set": {"EXCHANGE_TXN.NSE": {"delivery": 0.0000345, "mtf": 0.0000345, "intraday": 0.0000345,
                                  "futures": 0.00002, "options": 0.00053}},
     "note": "NSE top-slab rates from Jan 2021 (cash 0.00345%); smaller NSE revisions up to Sep 2024 are not "
             "tracked (under ₹0.25 per ₹1 lakh traded in cash)."},
    {"from": "2023-04-01", "verified": True,
     "set": {"STT.futures.sell": 0.000125, "STT.options.sell": 0.000625},
     "note": "Finance Act 2023: STT on futures 0.0125%, options 0.0625% of premium."},
    {"from": "2024-10-01", "verified": True,
     "set": {"STT.futures.sell": 0.0002, "STT.options.sell": 0.001,
             "EXCHANGE_TXN.NSE": {"delivery": 0.0000297, "mtf": 0.0000297, "intraday": 0.0000297,
                                  "futures": 0.0000173, "options": 0.0003503}},
     "note": "Finance (No. 2) Act 2024 STT (futures 0.02%, options 0.1%); SEBI true-to-label flat exchange "
             "charges (NSE cash 0.00297%)."},
    {"from": "2026-03-01", "verified": True,
     "set": {"EXCHANGE_TXN.NSE": {"delivery": 0.0000307, "mtf": 0.0000307, "intraday": 0.0000307,
                                  "futures": 0.0000183, "options": 0.0003553}},
     "note": "NSE transaction-charge revision effective 1 Mar 2026."},
    {"from": "2026-04-01", "verified": True,
     "set": {"STT.futures.sell": 0.0005, "STT.options.sell": 0.0015},
     "note": "Finance Act 2026: STT on futures 0.05%, options 0.15% of premium."},
]


def _build_eras() -> list:
    """[(start date, full rate dict, {component: approximation note})], oldest first."""
    import copy
    from datetime import date as _d
    cur, approx = copy.deepcopy(_BASELINE), dict(_BASELINE_APPROX)
    eras = [(_d.fromisoformat(RATE_HISTORY_START), copy.deepcopy(cur), dict(approx))]
    for e in RATE_HISTORY:
        for path, val in e["set"].items():
            keys = path.split(".")
            node = cur
            for k in keys[:-1]:
                node = node[k]
            node[keys[-1]] = copy.deepcopy(val)
            for comp in [c for c in approx if c == path or path.startswith(c + ".") or c.startswith(path + ".")]:
                del approx[comp]
            if not e["verified"]:
                approx[path] = e["note"]
        eras.append((_d.fromisoformat(e["from"]), copy.deepcopy(cur), dict(approx)))
    return eras


_ERAS = _build_eras()


def _as_date(on):
    from datetime import date as _d, datetime as _dt
    if isinstance(on, str):
        return _d.fromisoformat(on)
    return on.date() if isinstance(on, _dt) else on


def _era_index(on) -> int:
    k = 0
    for i, (start, _, _) in enumerate(_ERAS):
        if start <= on:
            k = i
    return k


def _approx_notes(approx: dict, exchange: str | None) -> list:
    other = {"NSE": "BSE", "BSE": "NSE"}.get((exchange or "").upper())
    return [n for c, n in approx.items() if not (other and c == f"EXCHANGE_TXN.{other}")]


def rates_on(on, exchange: str | None = None) -> dict:
    """Statutory and exchange rates in force on `on` (date or YYYY-MM-DD), plus `notes` listing the
    approximations in force. Dates before RATE_HISTORY_START use the first era and say so."""
    on = _as_date(on)
    start, rates, approx = _ERAS[_era_index(on)]
    notes = _approx_notes(approx, exchange)
    if on < _ERAS[0][0]:
        notes.append(f"{on} is before the rate history starts ({RATE_HISTORY_START}); June 2013 rates are used.")
    return dict(rates, era_from=start.isoformat(), notes=notes)


def rate_notes_between(start, end, exchange: str | None = None) -> dict:
    """Rate eras overlapping [start, end] and the approximations in force anywhere in it."""
    start, end = _as_date(start), _as_date(end)
    a, b = _era_index(start), _era_index(end)
    notes: list = []
    for k in range(a, b + 1):
        for n in _approx_notes(_ERAS[k][2], exchange):
            if n not in notes:
                notes.append(n)
    if start < _ERAS[0][0]:
        notes.append(f"Dates before {RATE_HISTORY_START} use June 2013 rates.")
    changes = [_ERAS[k][0].isoformat() for k in range(a + 1, b + 1)]
    return {"eras": b - a + 1, "changes_on": changes, "approximations": notes}


# ---------------------------------------------------------------------------
# Broker pricing (per executed order). Verified from official pricing pages.
#   pct  : fraction of order value     cap: max ₹ per order     min: min ₹ per order
#   flat : flat ₹ per order (overrides pct)
#   dp   : depository charge per scrip per sell day, BEFORE GST (delivery/MTF sells)
#   mtf_daily_rate: MTF interest per day on funded amount (fraction)
# ---------------------------------------------------------------------------
BROKERS = {
    "zerodha": {
        "name": "Zerodha (Kite)",
        "delivery": {"pct": 0.0},
        "intraday": {"pct": 0.0003, "cap": 20},
        "futures": {"pct": 0.0003, "cap": 20},
        "options": {"flat": 20},
        "mtf": {"pct": 0.003, "cap": 20},
        "dp": 13.0,  # ₹3.5 CDSL + ₹9.5 Zerodha
        "mtf_daily_rate": 0.0004,  # 0.04%/day
        "source": "https://zerodha.com/charges/",
    },
    "groww": {
        "name": "Groww",
        "delivery": {"pct": 0.001, "cap": 20, "min": 5},
        "intraday": {"pct": 0.001, "cap": 20, "min": 5},
        "futures": {"flat": 20},
        "options": {"flat": 20},
        "mtf": {"pct": 0.001, "cap": 20, "min": 5},
        "dp": 20.0,  # ₹16.5 Groww + ₹3.5 CDSL; ₹0 if debit value < ₹100
        "mtf_daily_rate": 0.1495 / 365,  # 14.95% p.a.
        "source": "https://groww.in/pricing",
    },
    "angelone": {
        "name": "Angel One",
        "delivery": {"pct": 0.001, "cap": 20, "min": 5},
        "intraday": {"pct": 0.001, "cap": 20, "min": 5},
        "futures": {"flat": 20},
        "options": {"flat": 20},
        "mtf": {"pct": 0.001, "cap": 20, "min": 5},
        "dp": 20.0,  # ₹16.5 Angel One + ₹3.5 CDSL
        "mtf_daily_rate": 0.00041,  # 0.041%/day
        "source": "https://www.angelone.in/pricing",
    },
    "upstox": {
        "name": "Upstox",
        "delivery": {"flat": 20},
        "intraday": {"pct": 0.001, "cap": 20},
        "futures": {"pct": 0.0005, "cap": 20},
        "options": {"flat": 20},
        "mtf": {"flat": 20},
        "dp": 20.0,  # ₹16.5 Upstox + ₹3.5 CDSL
        "mtf_daily_rate": 20 / 40000,  # ₹20/day per ₹40,000 funded
        "source": "https://upstox.com/brokerage-charges/",
    },
    "dhan": {
        "name": "Dhan",
        "delivery": {"pct": 0.0},
        "intraday": {"pct": 0.0003, "cap": 20},
        "futures": {"flat": 20},
        "options": {"flat": 20},
        "mtf": {"pct": 0.0003, "cap": 20},
        "dp": 12.5,
        "mtf_daily_rate": 0.1249 / 365,  # 12.49% p.a. up to ₹5L funded (tiered above)
        "source": "https://dhan.co/pricing/",
    },
}


def inr(x: float, decimals: int = 2) -> str:
    """Format a number with Indian digit grouping: 1234567.5 -> ₹12,34,567.50."""
    neg = x < 0
    s = f"{abs(x):.{decimals}f}"
    whole, _, frac = s.partition(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        whole = ",".join(groups + [tail])
    return ("-" if neg else "") + "₹" + whole + ("." + frac if frac else "")


def order_brokerage(profile: dict, order_value: float, segment: str) -> float:
    """Brokerage for ONE executed order of the given value."""
    if order_value <= 0:
        return 0.0
    if "flat" in profile:
        b = float(profile["flat"])
    else:
        b = order_value * profile.get("pct", 0.0)
        if "cap" in profile:
            b = min(b, profile["cap"])
        if b > 0 and "min" in profile:
            b = max(b, profile["min"])
    if segment in ("delivery", "intraday", "mtf"):
        b = min(b, order_value * SEBI_BROKERAGE_CAP_CASH)
    return b


def calculate(segment: str, buy: float, sell: float, qty: float, broker: str = "zerodha",
              exchange: str = "NSE", orders_per_side: int = 1, brokerage_override: dict | None = None,
              mtf_days: int = 0, mtf_funded: float = 0.0, dp_scrips: int = 1, on=None) -> dict:
    """Compute every charge for a round trip (one buy side + one sell side).

    on: a date (or YYYY-MM-DD) to use the statutory and exchange rates in force that day
    (RATE_HISTORY) instead of today's. Broker brokerage and DP charges are always today's.

    Pass buy=0 or sell=0 to price only one leg (e.g. an open position).
    For options, buy/sell are PREMIUMS per unit and qty is in units (lots x lot size).
    """
    if segment not in SEGMENTS:
        raise ValueError(f"segment must be one of {SEGMENTS}")
    exchange = exchange.upper()
    if exchange not in EXCHANGE_TXN:
        raise ValueError("exchange must be NSE or BSE")
    if broker not in BROKERS and not brokerage_override:
        raise ValueError(f"unknown broker '{broker}'. Known: {', '.join(BROKERS)}")
    bk = BROKERS.get(broker, {"name": "Custom", "dp": 0.0, "mtf_daily_rate": 0.0})
    profile = brokerage_override or bk.get(segment, {"pct": 0.0})

    if on is None:
        stt_r, exch_r, sebi_r, stamp_r, gst_r, basis = STT, EXCHANGE_TXN, SEBI_FEE, STAMP, GST, RATES_AS_OF
    else:
        rt = rates_on(on, exchange)
        stt_r, exch_r, sebi_r, stamp_r, gst_r = rt["STT"], rt["EXCHANGE_TXN"], rt["SEBI_FEE"], rt["STAMP"], rt["GST"]
        basis = f"rates in force on {_as_date(on).isoformat()} (era from {rt['era_from']})"

    buy_value = buy * qty
    sell_value = sell * qty
    turnover = buy_value + sell_value
    n = max(1, int(orders_per_side))

    brokerage = 0.0
    for side_value in (buy_value, sell_value):
        if side_value > 0:
            brokerage += n * order_brokerage(profile, side_value / n, segment)

    stt = buy_value * stt_r[segment]["buy"] + sell_value * stt_r[segment]["sell"]
    exch = turnover * exch_r[exchange][segment]
    sebi = turnover * sebi_r
    ipft = turnover * IPFT_NSE if exchange == "NSE" else 0.0
    stamp = buy_value * stamp_r[segment]
    gst = gst_r * (brokerage + exch + sebi + ipft)

    dp = 0.0
    if segment in ("delivery", "mtf") and sell_value > 0:
        dp_base = bk.get("dp", 0.0)
        if broker == "groww" and sell_value < 100:
            dp_base = 0.0
        dp = dp_base * (1 + gst_r) * max(1, dp_scrips)

    mtf_interest = 0.0
    if segment == "mtf" and mtf_days > 0 and mtf_funded > 0:
        mtf_interest = mtf_funded * bk.get("mtf_daily_rate", 0.0) * mtf_days

    total = brokerage + stt + exch + sebi + ipft + stamp + gst + dp + mtf_interest
    gross = (sell - buy) * qty if buy > 0 and sell > 0 else 0.0
    net = gross - total
    return {
        "segment": segment, "exchange": exchange, "broker": bk["name"], "broker_key": broker,
        "buy": buy, "sell": sell, "qty": qty, "buy_value": buy_value, "sell_value": sell_value,
        "turnover": turnover,
        "brokerage": brokerage, "stt": stt, "exchange_txn": exch, "sebi_fee": sebi,
        "ipft": ipft, "stamp_duty": stamp, "gst": gst, "dp_charges": dp,
        "mtf_interest": mtf_interest, "total_charges": total,
        "gross_pnl": gross, "net_pnl": net,
        "charges_pct_of_turnover": (total / turnover * 100) if turnover else 0.0,
        "charges_pct_of_gross": (total / abs(gross) * 100) if gross else None,
        "rates_as_of": RATES_AS_OF, "rates_basis": basis, "gst_rate": gst_r,
    }


def breakeven_sell(segment: str, buy: float, qty: float, **kw) -> float | None:
    """Sell price (or premium) at which a long round trip nets exactly zero.

    Returns None if no finite breakeven exists (should not happen for sane inputs)."""
    net = lambda px: calculate(segment, buy, px, qty, **kw)["net_pnl"]
    lo, hi = buy, max(buy * 1.5, buy + 1.0)
    for _ in range(64):                      # widen until the upper bound actually breaks even
        if net(hi) >= 0:
            break
        lo, hi = hi, hi * 2
    else:
        return None
    # Charges can jump (e.g. a DP charge that only applies above a sell value), so scan for the
    # FIRST bracket where net P&L turns non-negative before bisecting.
    steps = 400
    prev = lo
    for i in range(1, steps + 1):
        px = lo + (hi - lo) * i / steps
        if net(px) >= 0:
            lo, hi = prev, px
            break
        prev = px
    for _ in range(200):
        mid = (lo + hi) / 2
        if calculate(segment, buy, mid, qty, **kw)["net_pnl"] < 0:
            lo = mid
        else:
            hi = mid
    return hi


def breakeven_buy_for_short(segment: str, sell: float, qty: float, **kw) -> float | None:
    """Buy-back price at which a short round trip (sell first) nets exactly zero.

    Returns None when charges exceed the sale proceeds even at a near-zero buy-back."""
    if calculate(segment, sell * 1e-6, sell, qty, **kw)["net_pnl"] < 0:
        return None
    lo, hi = 0.0, sell
    for _ in range(200):
        mid = (lo + hi) / 2
        if calculate(segment, mid, sell, qty, **kw)["net_pnl"] < 0:
            hi = mid
        else:
            lo = mid
    return lo


ROWS = [("Brokerage", "brokerage"), ("STT", "stt"), ("Exchange txn", "exchange_txn"),
        ("SEBI fee", "sebi_fee"), ("IPFT", "ipft"), ("Stamp duty", "stamp_duty"),
        ("GST (18%)", "gst"), ("DP charges", "dp_charges"), ("MTF interest", "mtf_interest")]


def print_report(r: dict, be: float | None) -> None:
    when = r["rates_basis"] if r.get("rates_basis", "").startswith("rates in force") else f"rates as of {r['rates_as_of']}"
    print(f"\n{r['broker']} | {r['segment'].upper()} | {r['exchange']}  ({when})")
    unit = "premium" if r["segment"] == "options" else "price"
    print(f"Buy {unit} {inr(r['buy'])} x {r['qty']:g}  |  Sell {unit} {inr(r['sell'])} x {r['qty']:g}")
    print(f"Turnover: {inr(r['turnover'])}")
    print("-" * 46)
    for label, key in ROWS:
        if key == "gst" and r.get("gst_rate") is not None:
            label = f"{'GST' if r['gst_rate'] >= 0.18 else 'Service tax'} ({r['gst_rate'] * 100:g}%)"
        if abs(r[key]) >= 0.005 or key in ("brokerage", "stt", "gst"):
            print(f"{label:<16}{inr(r[key]):>30}")
    print("-" * 46)
    print(f"{'Total charges':<16}{inr(r['total_charges']):>30}")
    print(f"{'Gross P&L':<16}{inr(r['gross_pnl']):>30}")
    print(f"{'Net P&L':<16}{inr(r['net_pnl']):>30}")
    print(f"Charges = {r['charges_pct_of_turnover']:.4f}% of turnover"
          + (f", {r['charges_pct_of_gross']:.1f}% of gross P&L" if r["charges_pct_of_gross"] else ""))
    if r["buy"] > 0 and be is None:
        print("Breakeven: not reachable — charges exceed any realistic gain.")
    if be is not None:
        pts = be - r["buy"]
        print(f"Breakeven sell {unit}: {inr(be)} ({pts:+.2f} pts, {pts / r['buy'] * 100:+.3f}%)")
    print("Note: STT and stamp duty are rounded to the nearest rupee on contract notes.")
    if r.get("rates_basis", "").startswith("rates in force"):
        print("Broker brokerage and DP charges are today's pricing; only statutory/exchange rates are dated.")
        for n in rates_on(r["rates_basis"].split()[4], r["exchange"])["notes"]:
            print(f"Approximation: {n}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Indian trading charges calculator (NSE/BSE)")
    p.add_argument("--segment", required=True, choices=SEGMENTS)
    p.add_argument("--buy", type=float, default=0.0, help="buy price (options: premium per unit)")
    p.add_argument("--sell", type=float, default=0.0, help="sell price (options: premium per unit)")
    p.add_argument("--qty", type=float, required=True, help="quantity in units (F&O: lots x lot size)")
    p.add_argument("--broker", default="zerodha", help=f"{', '.join(BROKERS)}, custom, or all")
    p.add_argument("--exchange", default="NSE", choices=["NSE", "BSE", "nse", "bse"])
    p.add_argument("--orders", type=int, default=1, help="executed orders per side (default 1)")
    p.add_argument("--brokerage-pct", type=float, help="override: brokerage %% per order, e.g. 0.03")
    p.add_argument("--brokerage-cap", type=float, help="override: max ₹ per order")
    p.add_argument("--brokerage-flat", type=float, help="override: flat ₹ per order")
    p.add_argument("--mtf-days", type=int, default=0, help="MTF holding days (segment mtf)")
    p.add_argument("--mtf-funded", type=float, default=0.0, help="MTF amount funded by broker, ₹")
    p.add_argument("--on", metavar="YYYY-MM-DD",
                   help="use the statutory/exchange rates in force on this date (broker pricing stays current)")
    p.add_argument("--json", action="store_true", help="print JSON")
    a = p.parse_args(argv)
    if a.on:
        from datetime import date as _d
        try:
            _d.fromisoformat(a.on)
        except ValueError:
            print(f"error: --on must be YYYY-MM-DD, got {a.on!r}", file=sys.stderr)
            return 2

    override = None
    if a.brokerage_flat is not None:
        override = {"flat": a.brokerage_flat}
    elif a.brokerage_pct is not None:
        override = {"pct": a.brokerage_pct / 100}
        if a.brokerage_cap is not None:
            override["cap"] = a.brokerage_cap

    brokers = list(BROKERS) if a.broker == "all" else [a.broker]
    results = []
    for b in brokers:
        kw = dict(broker=b, exchange=a.exchange, orders_per_side=a.orders,
                  brokerage_override=override, mtf_days=a.mtf_days, mtf_funded=a.mtf_funded, on=a.on)
        try:
            r = calculate(a.segment, a.buy, a.sell, a.qty, **kw)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        be = None
        if a.buy > 0:
            be = breakeven_sell(a.segment, a.buy, a.qty, **kw)
            r["breakeven_sell"] = be
        if a.sell > 0:
            r["breakeven_buyback_if_short"] = breakeven_buy_for_short(a.segment, a.sell, a.qty, **kw)
        results.append((r, be))

    for r, _ in results:
        if r.get("sell", 0) > 0 and r.get("breakeven_buyback_if_short") is None:
            r["breakeven_buyback_if_short_note"] = "not achievable: charges exceed the sale proceeds"
    if a.json:
        out = [r for r, _ in results]
        print(json.dumps(out if len(out) > 1 else out[0], indent=2))
        return 0
    if len(results) == 1:
        print_report(*results[0])
        return 0
    # Comparison table
    print(f"\n{a.segment.upper()} on {a.exchange.upper()}: buy {a.buy:g} / sell {a.sell:g} x {a.qty:g}"
          f"  ({'statutory rates in force on ' + a.on if a.on else 'rates as of ' + RATES_AS_OF})")
    print(f"{'Broker':<16}{'Brokerage':>12}{'Total chg':>14}{'Net P&L':>16}{'Breakeven':>12}")
    for r, be in sorted(results, key=lambda t: t[0]["total_charges"]):
        print(f"{r['broker']:<16}{inr(r['brokerage']):>12}{inr(r['total_charges']):>14}"
              f"{inr(r['net_pnl']):>16}{(f'{be:.2f}' if be else '-'):>12}")
    print("Statutory charges (STT, exchange, SEBI, stamp, GST on those) are identical across brokers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
