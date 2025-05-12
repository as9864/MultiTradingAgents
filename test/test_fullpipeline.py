from infoharvester.orchestrator.gather_runner import run_full_pipeline
from coordinator.coordinator import Coordinator
from llm.llm_client import LLMClient
import pprint

def test_full_pipeline(symbol="AAPL"):
    print(f"🌀 [1/3] Running Orchestrator for: {symbol}")
    run_full_pipeline(symbol)

    print(f"\n🤖 [2/3] Running Coordinator Agents for: {symbol}")
    llm = LLMClient()
    coordinator = Coordinator(llm)
    result = coordinator.run({"symbol": symbol, "portfolio": {"cash": 10000}})

    print(f"\n📊 [3/3] Final Result Summary:\n{'='*50}")

    print("\n🔎 Research Summary:")
    print(result["research"]["summary"])

    print("\n📈 Analyst Summary:")
    print(result["analysis"]["technical_analysis"])
    print(f"Indicators: {result['analysis']['indicators']}")

    print("\n💡 Trader Decision:")
    print(result["trader"]["decision"])

    print("\n🔐 Risk Review:")
    print(result["risk_review"]["review"])
    print("Approved:", result["risk_review"]["approved"])

    print("\n💰 Final Portfolio:")
    pprint.pprint(result["final_portfolio"])

if __name__ == "__main__":
    for symbol in ["AAPL", "TSLA", "GOOGL"]:
        test_full_pipeline(symbol)