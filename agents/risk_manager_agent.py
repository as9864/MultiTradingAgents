from protocol.agent_base import AgentBase
from protocol.message import Message
from llm.llm_client import LLMClient
from simulator.trading_simulator import TradingSimulator

class RiskManagerAgent(AgentBase):
    def __init__(self, llm_client: LLMClient):
        super().__init__("RiskManager")
        self.llm = llm_client
        self.simulator = TradingSimulator()
        self.system_prompt = "You are a risk manager responsible for reviewing trade decisions."

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") != "review_decision":
            return Message(
                sender=self.name,
                receiver=message.sender,
                type="error",
                content={"error": "Invalid message type or action"}
            )

        symbol = message.content.get("symbol", "UNKNOWN")
        decision = message.content.get("decision", "HOLD")
        price = message.content.get("price", 0.0)
        quantity = message.content.get("quantity", 0)
        indicators = message.content.get("indicators", {})
        portfolio = message.content.get("portfolio", {})

        # 📩 프롬프트 구성
        user_prompt = (
            f"You are a risk manager agent reviewing a trade decision.\n"
            f"Stock: {symbol}\n"
            f"Trader's Decision: {decision}\n"
            f"Indicators: {indicators}\n"
            f"Portfolio Status: {portfolio}\n\n"
            f"Should this trade be approved or rejected?\n"
            f"Give a yes/no answer and a clear justification.\n"
            f"Respond in the format: 'Decision: APPROVE/REJECT\nReason: ...'"
        )

        response = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)
        approved = "APPROVE" in response.upper()

        result = {
            "symbol": symbol,
            "approved": approved,
            "review": response
        }

        # ✅ 승인된 경우 시뮬레이터 실행
        if approved and decision in ["BUY", "SELL"]:
            trade_result = self.simulator.execute_trade(
                symbol=symbol,
                action=decision,
                price=price,
                quantity=quantity,
                portfolio=portfolio
            )
            result["trade_execution"] = trade_result

        return Message(
            sender=self.name,
            receiver=message.sender,
            type="response",
            content=result
        )