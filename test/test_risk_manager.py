from agents.risk_manager_agent import RiskManagerAgent
from llm.llm_client import LLMClient


def test_risk_manager():
    llm = LLMClient(model="gpt-4-turbo")
    agent = RiskManagerAgent(llm)

    input_data = {
        "symbol": "AAPL",
        "decision": "BUY",
        "indicators": {
            "sma_5": 158.2,
            "rsi_14": 72.5  # overbought
        },
        "portfolio": {
            "cash": 2000,
            "positions": {
                "AAPL": {"quantity": 50, "avg_price": 150},
                "MSFT": {"quantity": 30, "avg_price": 300}
            }
        }
    }

    result = agent.run(input_data)

    print("\n⚠️ RiskManagerAgent Result:")
    print(f"Symbol: {result['symbol']}")
    print("Review Response:")
    print(result["review"])


if __name__ == "__main__":
    test_risk_manager()
