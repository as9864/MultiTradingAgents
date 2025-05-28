from protocol.agent_base import AgentBase
from protocol.message import Message
from llm.llm_client import LLMClient
from utils.portfolio_utils import evaluate_portfolio, can_allocate


class RiskManagerAgent(AgentBase):
    """
    Trader의 판단을 바탕으로 자산 기준, 비중 제한 등을 검토하여 승인 여부만 판단하는 에이전트
    실제 실행은 ExecutionAgent가 수행
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__("RiskManager")
        self.llm = llm_client
        self.system_prompt = self.load_prompt("prompts/risk_manager.txt")
        self.max_weight = 0.2  # 종목당 최대 비중 제한 (20%)

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        decision = input_data.get("decision", "HOLD")
        price = input_data.get("price", 0.0)
        quantity = input_data.get("quantity", 0)
        indicators = input_data.get("indicators", {})
        portfolio = input_data.get("portfolio", {})

        # 💰 자산 평가
        portfolio_eval = evaluate_portfolio(portfolio)

        # ✅ 정책 기반 리스크 검토
        if decision == "BUY":
            if portfolio["cash"] < price * quantity:
                return {
                    "agent": "RiskManager",
                    "symbol": symbol,
                    "approved": False,
                    "review": f"🚫 현금 부족: {portfolio['cash']:.2f} < {price * quantity:.2f}",
                    "portfolio_evaluation": portfolio_eval
                }

            if not can_allocate(symbol, price, quantity, portfolio_eval, max_weight=self.max_weight):
                new_weight = (portfolio_eval["per_asset"].get(symbol, 0) + price * quantity) / portfolio_eval["total_value"]
                return {
                    "agent": "RiskManager",
                    "symbol": symbol,
                    "approved": False,
                    "review": f"🚫 종목 비중 초과: 예상 {new_weight:.2%} > 제한 {self.max_weight:.0%}",
                    "portfolio_evaluation": portfolio_eval
                }

        # 🧠 LLM 판단
        user_prompt = (
            f"You are a risk manager agent reviewing a trade decision.\n"
            f"Stock: {symbol}\n"
            f"Trader's Decision: {decision}\n"
            f"Indicators: {indicators}\n"
            f"Portfolio Status: {portfolio}\n\n"
            f"Should this trade be approved or rejected?\n"
            f"Give a yes/no answer and a clear justification.\n"
            f"Respond in the format: 'Decision: APPROVE/REJECT\\nReason: ...'"
        )

        response = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)
        approved = "APPROVE" in response.upper()

        return {
            "agent": "RiskManager",
            "symbol": symbol,
            "approved": approved,
            "review": response,
            "portfolio_evaluation": portfolio_eval
        }

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") != "review":
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