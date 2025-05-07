import pandas as pd
from coordinator.coordinator import Coordinator
from llm.llm_client import LLMClient


def get_sample_price_data():
    return pd.DataFrame({
        "close": [150, 152, 149, 148, 151, 153, 155, 157, 156, 158, 160, 162, 161, 163, 165]
    })


def test_full_pipeline():
    llm = LLMClient(model="gpt-4-turbo")
    coordinator = Coordinator(llm)

    symbol = "AAPL"
    document = (
        "Apple Inc. announced strong Q1 earnings with a 12% YoY increase in revenue.\n"
        "Mac sales grew significantly, while iPhone sales slightly declined.\n"
        "The services sector showed strong expansion, but supply chain concerns remain in China."
    )
    price_data = get_sample_price_data()

    result = coordinator.run_pipeline(symbol, document, price_data)

    print("\n🧠 Coordinator Full Result:")
    print(f"Symbol: {result['symbol']}")
    print("\n--- Research Output ---")
    print(result["research"]["summary"])
    print("\n--- Technical Analysis ---")
    print(result["analysis"]["analysis"])
    print("\n--- Trader Decision ---")
    print(result["decision"]["decision"])


if __name__ == "__main__":
    test_full_pipeline()
