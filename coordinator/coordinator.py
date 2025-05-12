from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.trader_agent import TraderAgent
from agents.risk_manager_agent import RiskManagerAgent
from llm.llm_client import LLMClient
from infoharvester.market.data_loader import load_price_data


class Coordinator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.researcher = ResearcherAgent(llm_client)
        self.analyst = AnalystAgent(llm_client)
        self.trader = TraderAgent(llm_client)
        self.risk_manager = RiskManagerAgent(llm_client)

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        document = input_data.get("document", "")
        price_data = input_data.get("price_data")  # pandas DataFrame
        portfolio = input_data.get("portfolio", {})

        # 1️⃣ ResearcherAgent: 기업 정보 요약
        # researcher_output = self.researcher.run({
        #     "company_name": symbol,
        #     "document": document
        # })
        #
        # # 2️⃣ AnalystAgent: 기술 분석
        # analyst_output = self.analyst.run({
        #     "symbol": symbol,
        #     "price_data": price_data
        # })
        # 1️⃣ ResearcherAgent: 벡터 검색 기반 요약
        researcher_output = self.researcher.run({
            "symbol": symbol,
            "query": f"{symbol} recent financial outlook"
        })

        # 2️⃣ AnalystAgent: 가격 데이터 불러오기 + 지표 계산
        price_data = load_price_data(symbol)
        analyst_output = self.analyst.run({
            "symbol": symbol,
            "price_data": price_data
        })

        # 3️⃣ TraderAgent: 매수/매도 결정
        trader_input = {
            "symbol": symbol,
            "research_summary": researcher_output["summary"],
            "technical_analysis": analyst_output["technical_analysis"],
            "indicators": analyst_output["indicators"]
        }
        trader_output = self.trader.run(trader_input)

        # 4️⃣ RiskManagerAgent: 거래 승인 여부 확인 + 시뮬레이터 실행 포함
        risk_input = {
            "symbol": symbol,
            "decision": trader_output["decision"],
            "price": price_data.iloc[-1]["close"],
            "quantity": 10,  # 간단하게 고정
            "indicators": analyst_output["indicators"],
            "portfolio": portfolio
        }
        risk_output = self.risk_manager.run(risk_input)

        # 5️⃣ 전체 결과 통합
        return {
            "symbol": symbol,
            "research": researcher_output,
            "analysis": analyst_output,
            "trader": trader_output,
            "risk_review": risk_output,
            "final_portfolio": risk_output.get("trade_execution", {}).get("updated_portfolio", portfolio)
        }
