from agents.base_agent import BaseAgent
from llm.llm_client import LLMClient
from simulator.trading_simulator import TradingSimulator

class RiskManagerAgent(BaseAgent):
    """
    Trader의 결정에 대한 리스크 검토 및 승인/거절 판단
    input_data 예시:
    {
        "symbol": "AAPL",
        "decision": "BUY",
        "price": 160.0,
        "quantity": 10,
        "indicators": {...},
        "portfolio": {...}
    }
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__(llm_client)
        self.system_prompt = self.load_prompt("prompts/risk_manager.txt")
        self.simulator = TradingSimulator()  # ✅ 거래 시뮬레이터 포함

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        decision = input_data.get("decision", "HOLD")
        price = input_data.get("price", 0.0)
        quantity = input_data.get("quantity", 0)
        indicators = input_data.get("indicators", {})
        portfolio = input_data.get("portfolio", {})

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

        # ✅ 응답 내용에 'APPROVE'가 포함되어 있으면 승인된 것으로 처리
        approved = "APPROVE" in response.upper()

        result = {
            "agent": "RiskManager",
            "symbol": symbol,
            "approved": approved,  # ✅ 승인 여부를 bool 값으로 반환
            "review": response      # ✅ LLM의 원본 응답 내용 포함
        }

        # ✅ 거래 승인 시 포트폴리오 업데이트 수행
        if approved and decision in ["BUY", "SELL"]:
            trade_result = self.simulator.execute_trade(
                symbol=symbol,
                action=decision,
                price=price,
                quantity=quantity,
                portfolio=portfolio
            )
            result["trade_execution"] = trade_result

        return result
