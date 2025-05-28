from protocol.agent_base import AgentBase
from protocol.message import Message
from simulator.trading_simulator import TradingSimulator

class ExecutionAgent(AgentBase):
    """
    거래를 실제로 실행하는 역할.
    현재는 TradingSimulator를 통해 포트폴리오 상태만 시뮬레이션 함.
    """

    def __init__(self):
        super().__init__("ExecutionAgent")
        self.simulator = TradingSimulator()

    def run(self, input_data: dict) -> dict:
        # 시뮬레이터를 이용해 거래 실행
        result = self.simulator.execute_trade(
            symbol=input_data["symbol"],
            action=input_data["action"],
            price=input_data["price"],
            quantity=input_data["quantity"],
            portfolio=input_data["portfolio"]
        )
        return {
            "executed": True,
            "result": result
        }

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") not in ["BUY", "SELL"]:
            return Message(
                sender=self.name,
                receiver=message.sender,
                type="error",
                content={"error": "Invalid message type or action"}
            )

        result = self.run(message.content)

        return Message(
            sender=self.name,
            receiver=message.sender,
            type="response",
            content=result
        )