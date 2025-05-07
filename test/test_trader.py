from agents.trader_agent import TraderAgent
from llm.llm_client import LLMClient


def test_trader():
    llm = LLMClient(model="gpt-4-turbo")
    agent = TraderAgent(llm)

    input_data = {
        "symbol": "AAPL",
        "research_summary": (
            "Apple Inc. shows a healthy growth trajectory with strong service revenue and increasing Mac sales.\n"
            "However, iPhone sales are slightly down and supply chain issues in China remain a risk."
        ),
        "technical_analysis": (
            "The 5-day SMA is rising and the current price is above it.\n"
            "The RSI is at 62, indicating mild bullish momentum."
        ),
        "indicators": {
            "sma_5": 158.2,
            "rsi_14": 62.4
        }
    }

    result = agent.run(input_data)

    print("\n💼 TraderAgent Result:")
    print(f"Symbol: {result['symbol']}")
    print("Decision Output:")
    print(result["decision"])
    print(result["reason"])


if __name__ == "__main__":
    test_trader()
