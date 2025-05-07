import pandas as pd
from coordinator.coordinator import Coordinator
from llm.llm_client import LLMClient

def test_full_pipeline():
    llm = LLMClient(model="gpt-4-turbo")
    coordinator = Coordinator(llm)

    # 예시 시세 데이터 (최근 14일치 종가)
    prices = [154.1, 155.3, 153.9, 156.5, 157.1, 158.2, 159.0, 160.5, 162.3, 161.8, 163.0, 164.2, 165.1, 166.4]
    price_data = pd.DataFrame({"close": prices})

    # 포트폴리오 상태 예시
    portfolio = {
        "cash": 10000,
        "positions": {
            "AAPL": {"quantity": 20, "avg_price": 150.0}
        }
    }

    # 기업 리포트 요약 대상 문서
    document = (
        "Apple Inc. announced record revenue growth of 12% YoY in its Q1 report. "
        "Mac and services segments showed strong performance, while iPhone sales declined slightly. "
        "The company warned about ongoing supply chain disruptions in China."
    )

    # 전체 파이프라인 실행
    result = coordinator.run({
        "symbol": "AAPL",
        "document": document,
        "price_data": price_data,
        "portfolio": portfolio
    })

    # 결과 출력
    print("\n📊 [Researcher Summary]:")
    print(result["research"]["summary"])
    print("\n📈 [Analyst Output]:")
    print(result["analysis"]["technical_analysis"])
    print("\n💡 [Trader Decision]:")
    print(result["trader"]["decision"])
    print("Reason:", result["trader"]["reason"])
    print("\n⚠️ [Risk Manager Review]:")
    print(result["risk_review"]["review"])
    print("Approved:", result["risk_review"]["approved"])
    print("\n💼 [Updated Portfolio]:")
    print(result["final_portfolio"])

if __name__ == "__main__":
    test_full_pipeline()
