import pandas as pd
from agents.analyst_agent import AnalystAgent
from llm.llm_client import LLMClient

def get_sample_price_data():
    # 간단한 테스트용 주가 데이터 생성
    return pd.DataFrame({
        "close": [150, 152, 149, 148, 151, 153, 155, 157, 156, 158, 160, 162, 161, 163, 165]
    })


def test_analyst():
    llm = LLMClient(model="gpt-4-turbo")
    agent = AnalystAgent(llm)

    sample_data = {
        "symbol": "AAPL",
        "price_data": get_sample_price_data()
    }

    result = agent.run(sample_data)

    print("\n📈 AnalystAgent Result:")
    print(f"Symbol: {result['symbol']}")
    print("Indicators:")
    for key, val in result["indicators"].items():
        print(f"  {key}: {val:.2f}")
    print("\nLLM Analysis:")
    print(result["technical_analysis"])


if __name__ == "__main__":
    test_analyst()
