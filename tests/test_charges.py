import unittest

from _load import load

ch = load("trading-costs", "charges")


class TestCharges(unittest.TestCase):
    def test_zerodha_delivery_breakdown(self):
        r = ch.calculate("delivery", 1800, 1900, 100, broker="zerodha")
        self.assertAlmostEqual(r["brokerage"], 0.0)
        self.assertAlmostEqual(r["stt"], 370.0)              # 0.1% both sides
        self.assertAlmostEqual(r["exchange_txn"], 370000 * 0.0000307, places=4)
        self.assertAlmostEqual(r["stamp_duty"], 27.0)        # 0.015% on buy
        self.assertAlmostEqual(r["dp_charges"], 15.34, places=2)
        self.assertAlmostEqual(r["total_charges"], 426.18, places=1)

    def test_options_stt_on_sell_premium(self):
        r = ch.calculate("options", 120, 150, 130, broker="zerodha")
        self.assertAlmostEqual(r["stt"], 150 * 130 * 0.0015)  # 0.15% from 1 Apr 2026
        self.assertAlmostEqual(r["brokerage"], 40.0)
        self.assertAlmostEqual(r["total_charges"], 91.68, places=1)

    def test_futures_stt(self):
        r = ch.calculate("futures", 25000, 25100, 65, broker="dhan")
        self.assertAlmostEqual(r["stt"], 25100 * 65 * 0.0005)

    def test_intraday_pct_cap_and_minimum(self):
        small = ch.calculate("intraday", 100, 101, 10, broker="groww")      # 0.1% of 1000 = 1 -> min 5
        self.assertAlmostEqual(small["brokerage"], 10.0)
        big = ch.calculate("intraday", 2000, 2010, 500, broker="zerodha")   # 0.03% of 10L = 300 -> cap 20
        self.assertAlmostEqual(big["brokerage"], 40.0)

    def test_cash_brokerage_never_exceeds_2_5_pct(self):
        r = ch.calculate("delivery", 50, 0, 2, broker="upstox")              # flat 20 on a ₹100 order
        self.assertAlmostEqual(r["brokerage"], 2.5)

    def test_bse_futures_have_no_txn_charge(self):
        r = ch.calculate("futures", 80000, 80100, 20, broker="zerodha", exchange="BSE")
        self.assertEqual(r["exchange_txn"], 0.0)
        self.assertEqual(r["ipft"], 0.0)

    def test_breakeven_nets_to_zero(self):
        be = ch.breakeven_sell("delivery", 1800, 100, broker="zerodha")
        self.assertAlmostEqual(ch.calculate("delivery", 1800, be, 100, broker="zerodha")["net_pnl"], 0, places=2)
        self.assertGreater(be, 1800 * 1.002)  # delivery round trip costs > 0.2%

    def test_mtf_interest(self):
        r = ch.calculate("mtf", 500, 540, 400, broker="zerodha", mtf_days=20, mtf_funded=100000)
        self.assertAlmostEqual(r["mtf_interest"], 100000 * 0.0004 * 20)

    def test_override(self):
        r = ch.calculate("intraday", 1000, 1010, 100, broker="custom", brokerage_override={"flat": 10})
        self.assertAlmostEqual(r["brokerage"], 20.0)

    def test_inr_grouping(self):
        self.assertEqual(ch.inr(1234567.5), "₹12,34,567.50")
        self.assertEqual(ch.inr(-999), "-₹999.00")
        self.assertEqual(ch.inr(100000, 0), "₹1,00,000")

    def test_latest_rate_era_matches_current_constants(self):
        r = ch.rates_on("2099-01-01")
        for key in ("STT", "EXCHANGE_TXN", "SEBI_FEE", "STAMP", "GST"):
            self.assertEqual(r[key], getattr(ch, key), key)
        self.assertEqual(ch.calculate("futures", 100, 110, 1000, on="2099-01-01")["total_charges"],
                         ch.calculate("futures", 100, 110, 1000)["total_charges"])

    def test_dated_stt_eras(self):
        sell = lambda d: ch.calculate("futures", 0, 100, 1000, broker="zerodha", on=d)["stt"]
        self.assertAlmostEqual(sell("2023-03-31"), 100_000 * 0.0001)
        self.assertAlmostEqual(sell("2023-04-01"), 100_000 * 0.000125)
        self.assertAlmostEqual(sell("2024-10-01"), 100_000 * 0.0002)
        self.assertAlmostEqual(sell("2026-04-01"), 100_000 * 0.0005)
        opt = ch.calculate("options", 0, 100, 100, on="2024-09-30")["stt"]
        self.assertAlmostEqual(opt, 10_000 * 0.000625)

    def test_dated_gst_stamp_and_exchange(self):
        b = ch.calculate("delivery", 1000, 0, 100, broker="zerodha", on="2017-06-30")
        self.assertAlmostEqual(b["stamp_duty"], 100_000 * 0.0001)          # pre-2020 state-wise approximation
        self.assertAlmostEqual(b["exchange_txn"], 100_000 * 0.0000325)
        self.assertAlmostEqual(b["gst"], 0.15 * (b["exchange_txn"] + b["sebi_fee"] + b["ipft"]))
        a = ch.calculate("delivery", 1000, 0, 100, broker="zerodha", on="2020-07-01")
        self.assertAlmostEqual(a["stamp_duty"], 100_000 * 0.00015)
        self.assertAlmostEqual(a["gst"], 0.18 * (a["exchange_txn"] + a["sebi_fee"] + a["ipft"]))
        self.assertAlmostEqual(ch.calculate("delivery", 1000, 0, 100, on="2024-10-01")["exchange_txn"],
                               100_000 * 0.0000297)
        self.assertIn("rates in force on 2017-06-30", b["rates_basis"])

    def test_legs_on_dates_sum_to_round_trip(self):
        kw = {"broker": "groww", "on": "2022-05-10"}
        rt = ch.calculate("delivery", 500, 520, 37, **kw)["total_charges"]
        legs = (ch.calculate("delivery", 500, 0, 37, **kw)["total_charges"]
                + ch.calculate("delivery", 0, 520, 37, **kw)["total_charges"])
        self.assertAlmostEqual(rt, legs, places=9)

    def test_rate_notes_flag_approximations(self):
        old = ch.rates_on("2012-01-01", "NSE")
        self.assertTrue(any("before the rate history" in n for n in old["notes"]))
        self.assertTrue(any("Stamp duty" in n for n in old["notes"]))
        self.assertFalse(any("BSE" in n for n in old["notes"]))           # NSE run: BSE note filtered
        self.assertFalse(any("Stamp duty" in n for n in ch.rates_on("2021-01-01", "NSE")["notes"]))
        span = ch.rate_notes_between("2023-11-22", "2026-11-20", "NSE")
        self.assertEqual(span["changes_on"], ["2024-10-01", "2026-03-01", "2026-04-01"])
        self.assertEqual(span["eras"], 4)
        self.assertEqual(ch.rate_notes_between("2026-05-01", "2026-06-01", "NSE")["approximations"],
                         [n for n in ch.rates_on("2026-05-01", "NSE")["notes"]])

    def test_cli_runs(self):
        self.assertEqual(ch.main(["--segment", "intraday", "--buy", "100", "--sell", "101", "--qty", "10",
                                  "--broker", "all"]), 0)


if __name__ == "__main__":
    unittest.main()
