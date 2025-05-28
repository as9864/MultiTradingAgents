import unittest
from agents.execution_agent import ExecutionAgent
from protocol.message import Message


class TestExecutionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ExecutionAgent()

    def test_valid_buy_message(self):
        message = Message(
            sender="Trader",
            receiver="ExecutionAgent",
            type="request",
            content={
                "action": "BUY",
                "symbol": "AAPL",
                "price": 150.00,
                "quantity": 10,
                "portfolio": {"cash": 2000, "positions": {}}
            }
        )

        response = self.agent.handle_message(message)

        self.assertEqual(response.type, "response")
        self.assertEqual(response.sender, "ExecutionAgent")
        self.assertEqual(response.receiver, "Trader")
        self.assertTrue(response.content["executed"])
        self.assertIn("result", response.content)

    def test_valid_sell_message(self):
        message = Message(
            sender="Trader",
            receiver="ExecutionAgent",
            type="request",
            content={
                "action": "SELL",
                "symbol": "AAPL",
                "price": 150.00,
                "quantity": 5,
                "portfolio": {
                    "cash": 1000,
                    "positions": {
                        "AAPL": {
                            "quantity": 10,
                            "avg_price": 140.00  # 예시 평균단가
                        }
                    }
                }
            }
        )

        response = self.agent.handle_message(message)

        self.assertEqual(response.type, "response")
        self.assertTrue(response.content["executed"])
        self.assertIn("result", response.content)

    def test_invalid_action(self):
        message = Message(
            sender="Trader",
            receiver="ExecutionAgent",
            type="request",
            content={
                "action": "HOLD",  # ❌ 지원하지 않는 액션
                "symbol": "AAPL",
                "price": 150.00,
                "quantity": 10,
                "portfolio": {}
            }
        )

        response = self.agent.handle_message(message)

        self.assertEqual(response.type, "error")
        self.assertEqual(response.content["error"], "Invalid message type or action")

    def test_invalid_type(self):
        message = Message(
            sender="Trader",
            receiver="ExecutionAgent",
            type="notify",  # ❌ 잘못된 메시지 타입
            content={
                "action": "BUY",
                "symbol": "AAPL",
                "price": 150.00,
                "quantity": 10,
                "portfolio": {}
            }
        )

        response = self.agent.handle_message(message)

        self.assertEqual(response.type, "error")
        self.assertEqual(response.content["error"], "Invalid message type or action")


if __name__ == '__main__':
    unittest.main()