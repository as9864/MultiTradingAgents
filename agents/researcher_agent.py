from agents.base_agent import BaseAgent
from llm.llm_client import LLMClient

class ResearcherAgent(BaseAgent):
    """
    기업 뉴스, 리포트, 재무제표 등 텍스트 데이터를 요약하고 평가하는 역할
    input_data는 다음과 같은 구조를 가질 수 있음:
    {
        "company_name": "Apple",
        "document": "Apple released its Q1 earnings..."
    }
    """



    def __init__(self, llm_client: LLMClient):
        super().__init__(llm_client)
        self.system_prompt = self.load_prompt("prompts/researcher.txt")

    def run(self, input_data: dict) -> dict:
        document = input_data.get("document", "")
        company = input_data.get("company_name", "Unknown Company")

        user_prompt = f"Please analyze the following report about {company} and summarize key findings, risks, and opportunities.\n\n{document}"

        summary = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)

        return {
            "agent": "Researcher",
            "company": company,
            "summary": summary
        }
