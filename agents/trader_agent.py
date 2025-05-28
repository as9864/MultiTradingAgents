from protocol.agent_base import AgentBase
from protocol.message import Message
from llm.llm_client import LLMClient

class TraderAgent(AgentBase):
    """
    Researcher와 Analyst 정보를 바탕으로 판단을 내리고,
    RiskManager로부터 승인받은 후 ExecutionAgent에게 실행을 요청함
    """

    def __init__(self, llm_client: LLMClient, router):
        super().__init__("Trader")
        self.llm = llm_client
        self.system_prompt = self.load_prompt("prompts/trader.txt")
        self.router = router

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        research = input_data.get("research_summary", "")
        tech = input_data.get("technical_analysis", "")
        indicators = input_data.get("indicators", {})
        portfolio = input_data.get("portfolio", {})
        price = input_data.get("price", 0.0)
        quantity = input_data.get("quantity", 10)  # 기본 10주

        user_prompt = (
            f"You are an investment decision agent.\n"
            f"Stock: {symbol}\n\n"
            f"--- Research Summary ---\n{research}\n\n"
            f"--- Technical Analysis ---\n{tech}\n\n"
            f"--- Indicators ---\n{indicators}\n\n"
            f"Based on the above, decide whether to BUY, HOLD, or SELL the stock.\n"
            f"Explain your reasoning clearly."
        )

        decision = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)

        # ✅ 판단 결과에서 BUY/SELL 추출
        action = "HOLD"
        if "BUY" in decision.upper():
            action = "BUY"
        elif "SELL" in decision.upper():
            action = "SELL"

        # ✅ RiskManager에 승인 요청
        risk_input = {
            "symbol": symbol,
            "decision": action,
            "price": price,
            "quantity": quantity,
            "indicators": indicators,
            "portfolio": portfolio
        }

        # risk_result = self.router.dispatch("RiskManager", "review", risk_input)
        risk_msg = Message(
            sender=self.name,
            receiver="RiskManager",
            type="request",
            content={
                "action": "review",
                "symbol": symbol,
                "decision": action,
                "price": price,
                "quantity": quantity,
                "indicators": indicators,
                "portfolio": portfolio
            }
        )
        risk_response = self.router.dispatch(risk_msg)
        risk_result = risk_response.content  # ✅ 이 라인 추가

        print("risk_result : ", risk_result)



        if "approved" not in risk_result:
            return {
                "agent": "Trader",
                "symbol": symbol,
                "decision": action,
                "approved": False,
                "reason": f"❌ RiskManager 반려\n\n{risk_result['review']}",
                "portfolio": portfolio
            }

        # ExecutionAgent 호출 메시지 구성
        exec_msg = Message(
            sender=self.name,
            receiver="ExecutionAgent",
            type="request",
            content={
                "action": action,
                "symbol": symbol,
                "price": price,
                "quantity": quantity,
                "portfolio": portfolio
            }
        )
        print("exec_msg : " , exec_msg)

        print("portfolio: ", portfolio)

        exec_response = self.router.dispatch(exec_msg)
        exec_result = exec_response.content

        print("exec_result : " , exec_result)

        return {
            "agent": "Trader",
            "symbol": symbol,
            "decision": action,
            "approved": True,
            "reason": decision,
            "execution": exec_result,
            "portfolio": exec_result["result"].get("updated_portfolio", portfolio)
        }

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") != "decide":
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