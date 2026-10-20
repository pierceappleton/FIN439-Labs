"""Run from any directory: python labs/lab-14/verify_labs.py."""
import importlib.util
from pathlib import Path
import unittest


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
m = load("mandate", ROOT / "lab-13" / "mandate.py")
p = load("portfolio", ROOT / "lab-14" / "portfolio.py")


class RequiredChecks(unittest.TestCase):
    def test_mandate_known_answers(self):
        self.assertEqual(m.reserve_minimum(), 3.0)
        expected = {"A": ([100, 0, 14, 100, 0], 0),
                    "B": ([100, 0, 1, 85, 9], 3),
                    "C": ([100, 0, 2, 100, 8], 1),
                    "D": ([100, 0, 100, 100, 0], 0),
                    "E": ([100, 0, 0, 100, 0], 1)}
        for name, (values, failures) in expected.items():
            with self.subTest(candidate=name):
                results = m.check_candidate(m.CANDIDATES[name])
                self.assertEqual([value for _, value, _ in results], values)
                self.assertEqual(sum(not passed for _, _, passed in results), failures)

    def test_negative_cash_probe(self):
        weights = {**m.CANDIDATES["A"], "Cash": -2, "Global equity index fund": 64}
        results = m.check_candidate(weights)
        self.assertEqual([value for _, value, _ in results], [100, -2, 10, 100, 0])
        self.assertEqual([passed for _, _, passed in results], [True, False, True, True, True])

    def test_baseline_known_answers(self):
        expected = {"Benchmark": ([0, 0, 40, 60], 6.80, 10.46, 0.0, True),
                    "Equal weight": ([25, 25, 25, 25], 5.20, 5.21, 50.0, False),
                    "Inverse volatility": ([84.3, 6.0, 7.0, 2.6], 3.77, 1.05, 90.3, False)}
        covariance = p.covariance_matrix(p.SLEEVES, p.CORRELATIONS)
        for name, weights in p.portfolios(p.SLEEVES).items():
            with self.subTest(portfolio=name):
                ew, er, ev, reserve, meets = expected[name]
                self.assertAlmostEqual(sum(weights), 1)
                self.assertEqual([round(w * 100, 1) for w in weights], ew)
                value = p.expected_return(weights, p.SLEEVES)
                self.assertEqual(round(value * 100, 2), er)
                self.assertEqual(round(p.portfolio_volatility(weights, covariance) * 100, 2), ev)
                self.assertEqual(round(p.reserve_weight(weights, p.SLEEVES) * 100, 1), reserve)
                self.assertEqual(p.meets_objective(value, p.OBJECTIVE_RETURN), meets)

    def test_correlation_change(self):
        correlations = [list(row) for row in p.CORRELATIONS]
        correlations[2][3] = correlations[3][2] = 0.50
        covariance = p.covariance_matrix(p.SLEEVES, correlations)
        benchmark = p.portfolios(p.SLEEVES)["Benchmark"]
        self.assertEqual(round(p.portfolio_volatility(benchmark, covariance) * 100, 2), 11.00)

    def test_bad_correlation_refused(self):
        for value in (1.3, -1.3):
            correlations = [list(row) for row in p.CORRELATIONS]
            correlations[2][3] = correlations[3][2] = value
            with self.assertRaisesRegex(ValueError, "between -1 and 1"):
                p.covariance_matrix(p.SLEEVES, correlations)

    def test_asymmetry_refused(self):
        correlations = [list(row) for row in p.CORRELATIONS]
        correlations[2][3] = 0.50
        with self.assertRaisesRegex(ValueError, "symmetric"):
            p.covariance_matrix(p.SLEEVES, correlations)


if __name__ == "__main__":
    unittest.main(verbosity=2)
