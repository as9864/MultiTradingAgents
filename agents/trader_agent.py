from protocol.agent_base import AgentBase
from protocol.message import Message
from llm.llm_client import LLMClient
import re

class TraderAgent(AgentBase):
    """
    Researcher와 Analyst 결과를 종합해 매수/보류/매도 판단을 내리는 에이전트
    input_data 예시:
    {
        "symbol": "AAPL",
        "research_summary": "...",
        "technical_analysis": "...",
        "indicators": { "sma_5": 158.2, "rsi_14": 62.4 }
    }
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__("Trader")
        self.llm = llm_client
        self.system_prompt = self.load_prompt("prompts/trader.txt")

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        research = input_data.get("research_summary", "")
        tech = input_data.get("technical_analysis", "")
        indicators = input_data.get("indicators", {})

        user_prompt = (
            f"You are an investment decision agent.\n"
            f"Stock: {symbol}\n\n"
            f"--- Research Summary ---\n{research}\n\n"
            f"--- Technical Analysis ---\n{tech}\n\n"
            f"--- Indicators ---\n{indicators}\n\n"
            f"Based on the above, decide whether to BUY, HOLD, or SELL the stock.\n"
            f"Explain your reasoning clearly.\n"
            f"Respond in the format:\nDecision: <BUY/SELL/HOLD>\nReason: <Explanation>"
        )

        response = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)

        # ✅ 정규표현식으로 응답 파싱
        decision_match = re.search(r"Decision:\s*(BUY|SELL|HOLD)", response.upper())
        reason_match = re.search(r"Reason:\s*(.+)", response, re.DOTALL)

        decision = decision_match.group(1).capitalize() if decision_match else "HOLD"
        reason = reason_match.group(1).strip() if reason_match else response.strip()

        return {
            "agent": "Trader",
            "symbol": symbol,
            "decision": decision,
            "reason": reason
        }

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") != "make_decision":
            return Message(
                sender=self.name,
                receiver=message.sender,
                type="error",
                content={"error": "Invalid message type or action"}
            )

        symbol = message.content.get("symbol", "UNKNOWN")
        research = message.content.get("research", "")
        tech = message.content.get("technical", "")
        indicators = message.content.get("indicators", {})

        user_prompt = (
            f"You are an investment decision agent.\n"
            f"Stock: {symbol}\n\n"
            f"--- Research Summary ---\n{research}\n\n"
            f"--- Technical Analysis ---\n{tech}\n\n"
            f"--- Indicators ---\n{indicators}\n\n"
            f"Based on the above, decide whether to BUY, HOLD, or SELL the stock.\n"
            f"Explain your reasoning clearly."
        )

        response = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)

        return Message(
            sender=self.name,
            receiver=message.sender,
            type="response",
            content={
                "agent": "Trader",
                "symbol": symbol,
                "decision": response,
                "reason": response  # 지금은 응답 전체가 reasoning 포함
            }
        )