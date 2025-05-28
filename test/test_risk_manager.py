from unittest import TestCase
from unittest.mock import patch
from protocol.message import Message
from agents.risk_manager_agent import RiskManagerAgent
from llm.llm_client import LLMClient


class TestRiskManagerAgent(TestCase):
    def setUp(self):
        self.agent = RiskManagerAgent(llm_client=LLMClient())

    @patch("agents.risk_manager_agent.can_allocate")
    @patch("agents.risk_manager_agent.evaluate_portfolio")
    def test_approved_trade(self, mock_evaluate, mock_can_allocate):
        mock_evaluate.return_value = {
            "total_value": 1000.0,
            "per_asset": {"AAPL": 0.0}
        }
        mock_can_allocate.return_value = True

        input_data = {
            "action": "review",
            "symbol": "AAPL",
            "decision": "BUY",
            "price": 100.0,
            "quantity": 5,
            "indicators": {},
            "portfolio": {
                "cash": 1000.0,
                "holdings": {},
            }
        }

        message = Message(
            sender="Trader",
            receiver="RiskManager",
            type="request",
            content=input_data
        )

        response = self.agent.handle_message(message)

        self.assertEqual(response.type, "response")
        self.assertTrue(response.content["approved"])
        self.assertIn("portfolio_evaluation", response.content)
