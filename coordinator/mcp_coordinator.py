from protocol.message import Message
from protocol.router import MessageRouter

class MCPCoordinator:
    def __init__(self, router: MessageRouter):
        self.router = router
        self.state = {}  # 공유 상태 저장소

    def run(self, symbol: str, portfolio: dict = None) -> dict:
        portfolio = portfolio or {"cash": 10000}
        self.state["symbol"] = symbol
        self.state["portfolio"] = portfolio

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
        print("self.state['analysis'] : " , self.state["analysis"])
        # 3️⃣ Trader 요청
        trader_msg = Message(
            sender="Coordinator",
            receiver="Trader",
            type="request",
            content={
                "action": "make_decision",
                "symbol": symbol,
                "research": self.state["research"]["summary"],
                "technical": self.state["analysis"]["technical_analysis"],
                "indicators": self.state["analysis"]["indicators"]
            }
        )
        trader_response = self.router.dispatch(trader_msg)
        self.state["trader"] = trader_response.content

        # 4️⃣ RiskManager 요청
        risk_msg = Message(
            sender="Coordinator",
            receiver="RiskManager",
            type="request",
            content={
                "action": "review_decision",
                "symbol": symbol,
                "decision": self.state["trader"]["decision"],
                "price": self.state["analysis"]["indicators"]["latest_close"],
                "quantity": 10,
                "indicators": self.state["analysis"]["indicators"],
                "portfolio": self.state["portfolio"]
            }
        )
        risk_response = self.router.dispatch(risk_msg)
        self.state["risk_review"] = risk_response.content

        # 💰 최종 포트폴리오 갱신
        self.state["final_portfolio"] = self.state["risk_review"].get("trade_execution", {}).get(
            "updated_portfolio", self.state["portfolio"]
        )

        return self.state
