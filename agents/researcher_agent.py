# from agents.base_agent import BaseAgent
from protocol.agent_base import AgentBase
from protocol.message import Message
from llm.llm_client import LLMClient
from summarizer.research_summarizer import ResearchSummarizer

class ResearcherAgent(AgentBase):
    """
    기업 뉴스, 리포트, 재무제표 등 텍스트 데이터를 요약하고 평가하는 역할
    input_data는 다음과 같은 구조를 가질 수 있음:
    {
        "company_name": "Apple",
        "document": "Apple released its Q1 earnings..."
    }
    """



    # def __init__(self, llm_client: LLMClient):
    #     super().__init__(llm_client)
    #     self.system_prompt = self.load_prompt("prompts/researcher.txt")
    #
    # def run(self, input_data: dict) -> dict:
    #     document = input_data.get("document", "")
    #     company = input_data.get("company_name", "Unknown Company")
    #
    #     user_prompt = f"Please analyze the following report about {company} and summarize key findings, risks, and opportunities.\n\n{document}"
    #
    #     summary = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)
    #
    #     return {
    #         "agent": "Researcher",
    #         "company": company,
    #         "summary": summary
    #     }
    def __init__(self, llm_client: LLMClient):
        super().__init__("Researcher")
        self.summarizer = ResearchSummarizer(llm_client)

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        query = input_data.get("query", f"{symbol} recent earnings and outlook")

        # 🔄 RAG 기반 뉴스 요약 수행
        summary_data = self.summarizer.summarize(
            symbol=symbol,
            query=query,
            top_k=5
        )

        return {
            "agent": "Researcher",
            "symbol": symbol,
            "summary": summary_data["summary"],
            "sources": summary_data["sources"]
        }

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") != "summarize":
            return Message(
                sender=self.name,
                receiver=message.sender,
                type="error",
                content={"error": "Invalid message type or action"}
            )

        symbol = message.content.get("symbol")
        query = message.content.get("query", f"{symbol} recent financial summary")

        summary_data = self.summarizer.summarize(symbol=symbol, query=query)

        return Message(
            sender=self.name,
            receiver=message.sender,
            type="response",
            content={
                "symbol": symbol,
                "summary": summary_data["summary"],
                "sources": summary_data["sources"]
            }
        )