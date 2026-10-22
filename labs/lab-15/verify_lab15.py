"""Known answers, feasibility, CSV validation and Streamlit integration checks."""
import io
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lab-14"))
import portfolio as p


class EngineChecks(unittest.TestCase):
    def test_meridian_and_stress(self):
        base = p.search(p.SLEEVES, p.CORRELATIONS)
        self.assertEqual(base["weights"], (0, .2, .25, .55))
        self.assertEqual(round(base["expected_return"] * 100, 2), 6.51)
        self.assertEqual(round(base["volatility"] * 100, 2), 9.44)
        changed = list(p.SLEEVES)
        changed[3] = (changed[3][0], .07, changed[3][2])
        stress = p.search(changed, p.CORRELATIONS)
        self.assertEqual(stress["weights"], (0, .1, .1, .8))
        self.assertEqual(round(stress["expected_return"] * 100, 2), 6.53)
        self.assertEqual(round(stress["volatility"] * 100, 2), 12.94)
        self.assertAlmostEqual(p.largest_weight_change(base, stress), 25)
        corr = [list(row) for row in p.CORRELATIONS]
        corr[2][3] = corr[3][2] = .5
        result = p.search(p.SLEEVES, corr)
        self.assertEqual(result["weights"], (0, .4, 0, .6))
        self.assertEqual(round(result["expected_return"] * 100, 2), 6.52)
        self.assertEqual(round(result["volatility"] * 100, 2), 9.73)

    def test_feasibility_and_reserve(self):
        self.assertIsNone(p.search(p.SLEEVES, p.CORRELATIONS, .10))
        self.assertIsNone(p.search(p.SLEEVES, p.CORRELATIONS, reserve_eligible=set()))
        self.assertIsNotNone(p.search(p.SLEEVES, p.CORRELATIONS,
                                     reserve_minimum=0, reserve_eligible=set()))
        for weights in p.weight_grid(4):
            self.assertAlmostEqual(sum(weights), 1)
            self.assertGreaterEqual(min(weights), 0)

    def test_csv_and_windows(self):
        results = []
        for last, count in ((False, 59), (True, 36)):
            sleeves, corr, meta = p.estimate_from_csv(ROOT / "lab-14/prices.csv", last)
            self.assertEqual(meta["returns"], count)
            p.validate_inputs(sleeves, corr)
            result = p.search(sleeves, corr, reserve_eligible={"BIL", "IEF"})
            self.assertEqual(result["weights"], (.85, 0, 0, .15) if last else (.6, 0, 0, .4))
            results.append(result)
        self.assertAlmostEqual(p.largest_weight_change(*results), 25)
        bad = "Date,A,B,C\n2026-02-01,1,2,3\n2026-01-01,2,3,4\n2026-03-01,3,4,5"
        with self.assertRaisesRegex(ValueError, "oldest first"):
            p.estimate_from_csv(io.StringIO(bad))

    def test_page(self):
        from streamlit.testing.v1 import AppTest
        at = AppTest.from_file(str(Path(__file__).resolve().with_name("app.py")), default_timeout=30).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value, "6.51%")
        equity = next(x for x in at.number_input if "Global equity" in x.label)
        equity.set_value(7.0).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[-1].value, "25.00")
        at.checkbox[0].check().run()
        self.assertFalse(at.exception)
        at.toggle[0].set_value(True).run()
        self.assertFalse(at.exception)

    def test_page_follows_engine_file(self):
        from streamlit.testing.v1 import AppTest
        engine_file = ROOT / "lab-14/portfolio.py"
        original = engine_file.read_text(encoding="utf-8")
        changed = original.replace("1.00, 0.25)", "1.00, 0.50)").replace(
            "-0.10, 0.25, 1.00)", "-0.10, 0.50, 1.00)")
        self.assertNotEqual(original, changed)
        try:
            engine_file.write_text(changed, encoding="utf-8")
            # Equal-length edits within one second can reuse timestamp-based bytecode.
            Path(p.__cached__).unlink(missing_ok=True)
            at = AppTest.from_file(str(Path(__file__).resolve().with_name("app.py")), default_timeout=30).run()
            self.assertFalse(at.exception)
            self.assertEqual(at.metric[0].value, "6.52%")
            self.assertEqual(at.metric[1].value, "9.73%")
        finally:
            engine_file.write_text(original, encoding="utf-8")
            Path(p.__cached__).unlink(missing_ok=True)
            import importlib
            importlib.reload(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
