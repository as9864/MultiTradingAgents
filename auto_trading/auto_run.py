from coordinator.mcp_coordinator import MCPCoordinator
from protocol.router import MessageRouter
from agents.trader_agent import TraderAgent
from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.risk_manager_agent import RiskManagerAgent
from llm.llm_client import LLMClient
import yaml
from auto_trading.result_logger import save_result

# auto/auto_run.py
def load_config(path="auto_trading/trading_config.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_analysis(symbol):
    llm = LLMClient()
    router = MessageRouter({
        "Researcher": ResearcherAgent(llm),
        "Analyst": AnalystAgent(llm),
        "Trader": TraderAgent(llm),
        "RiskManager": RiskManagerAgent(llm),
    })
    coordinator = MCPCoordinator(router)
    result = coordinator.run(symbol)

    print("\n🧾 매매 요약 (모의 실행)")
    print("종목:", result["symbol"])
    print("📈 Trader 판단:", result["trader"]["decision"])
    print("🔐 RiskManager 승인여부:", result["risk_review"]["approved"])
    print("💰 최종 포트폴리오:", result["final_portfolio"])

    save_result(result)  # 📌 CSV 저장 추가

    return result

if __name__ == "__main__":
    config = load_config()
    run_analysis(config.get("symbol", "AAPL"))