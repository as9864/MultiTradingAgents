from protocol.message import Message
from protocol.router import MessageRouter

class MCPCoordinator:
    def __init__(self, router: MessageRouter):
        self.router = router
        self.state = {}

    def run(self, symbol: str, portfolio: dict = None) -> dict:
        portfolio = portfolio or {"cash": 10000}
        self.state["symbol"] = symbol
        self.state["portfolio"] = portfolio


        print("mcp_coordinator portfolio : " ,self.state["portfolio"] )

        # 1️⃣ Research 요청
        research_msg = Message(
            sender="Coordinator",
            receiver="Researcher",
            type="request",
            content={
                "action": "summarize",
                "symbol": symbol,
                "query": f"{symbol} latest financial outlook"
            }
        )
        research_response = self.router.dispatch(research_msg)
        self.state["research"] = research_response.content

        # 2️⃣ Analyst 요청
        analyst_msg = Message(
            sender="Coordinator",
            receiver="Analyst",
            type="request",
            content={
                "action": "analyze",
                "symbol": symbol
            }
        )
        analyst_response = self.router.dispatch(analyst_msg)
        self.state["analysis"] = analyst_response.content

        # 3️⃣ Trader 요청 → 내부에서 RiskManager + Execution까지 호출
        trader_msg = Message(
            sender="Coordinator",
            receiver="Trader",
            type="request",
            content={
                "action": "decide",  # ← 여기 이름 주의
                "symbol": symbol,
                "research_summary": self.state["research"]["summary"],
                "technical_analysis": self.state["analysis"]["technical_analysis"],
                "indicators": self.state["analysis"]["indicators"],
                "price": self.state["analysis"]["indicators"]["latest_close"],
                "quantity": 10,
                "portfolio": self.state["portfolio"]
            }
        )
        trader_response = self.router.dispatch(trader_msg)
        self.state["trader"] = trader_response.content

        # 4️⃣ RiskManager 결과는 TraderAgent 안에서 호출되므로 따로 메시지 필요 없음
        # 단, trader_response 내에 approved / review 등이 포함되어 있어야 함
        self.state["risk_review"] = {
            "approved": self.state["trader"].get("approved", False),
            "review": self.state["trader"].get("reason", "N/A")
        }

        # 💰 최종 포트폴리오 (ExecutionAgent 결과 포함)
        self.state["final_portfolio"] = self.state["trader"].get("portfolio", portfolio)
        print("mcp_coordinator final_portfolio : ", self.state["final_portfolio"])

        return self.state