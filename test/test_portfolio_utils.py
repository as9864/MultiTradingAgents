import unittest
from unittest.mock import patch
from utils import portfolio_utils


class TestPortfolioUtils(unittest.TestCase):

    @patch("utils.portfolio_utils.fetch_price_history")
    def test_evaluate_portfolio(self, mock_fetch_price):
        # ✅ 가짜 가격 리턴
        mock_fetch_price.side_effect = lambda symbol: {
            "AAPL": 150.0,
            "GOOG": 1200.0
        }.get(symbol, 0.0)

        portfolio = {
            "cash": 500.0,
            "AAPL": 2,   # $300
            "GOOG": 1    # $1200
        }

        result = portfolio_utils.evaluate_portfolio(portfolio)

        self.assertAlmostEqual(result["total_value"], 500 + 300 + 1200)
        self.assertEqual(result["per_asset"]["AAPL"], 300.0)
        self.assertEqual(result["per_asset"]["GOOG"], 1200.0)
        self.assertEqual(result["per_asset"]["cash"], 500.0)

    def test_can_allocate_within_limit(self):
        portfolio_eval = {
            "total_value": 10000,
            "per_asset": {
                "AAPL": 1000
            }
        }
        # ✅ 현재 1000 + 새로 500 = 1500 → 15% < 20%
        result = portfolio_utils.can_allocate("AAPL", price=50, quantity=10, portfolio_eval=portfolio_eval, max_weight=0.2)
        self.assertTrue(result)

    def test_can_allocate_exceeds_limit(self):
        portfolio_eval = {
            "total_value": 10000,
            "per_asset": {
                "AAPL": 1000
            }
        }
        # ❌ 1000 + 1500 = 2500 → 25% > 20%
        result = portfolio_utils.can_allocate("AAPL", price=150, quantity=10, portfolio_eval=portfolio_eval, max_weight=0.2)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()