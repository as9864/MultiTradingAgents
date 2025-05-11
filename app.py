import streamlit as st
import pandas as pd
import re

from llm.llm_client import LLMClient
from coordinator.coordinator import Coordinator

st.set_page_config(page_title="LLM 기반 트레이딩 에이전트", layout="wide")

# 제목
st.title("🤖 LLM 기반 멀티 에이전트 트레이딩 시스템")

# 사용자 입력
symbol = st.text_input("종목 코드 (예: AAPL)", value="AAPL")
document = st.text_area("기업 보고서 또는 뉴스 텍스트", height=200, value="""
Apple Inc. announced record revenue growth of 12% YoY in its Q1 report.
Mac and services segments showed strong performance, while iPhone sales declined slightly.
The company warned about ongoing supply chain disruptions in China.
""")

# 가격 데이터 자동 생성
st.subheader("📈 시세 데이터 (최근 14일)")
default_prices = [154.1, 155.3, 153.9, 156.5, 157.1, 158.2, 159.0, 160.5, 162.3, 161.8, 163.0, 164.2, 165.1, 166.4]
price_data = pd.DataFrame({"close": default_prices})
st.line_chart(price_data["close"])

# 포트폴리오 설정
st.subheader("💼 포트폴리오 구성")
cash = st.number_input("보유 현금", value=10000)
positions = {
    "AAPL": {"quantity": 20, "avg_price": 150.0}
}
st.write("보유 종목:", positions)


if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

# 실행
if st.button("🚀 에이전트 실행"):
    st.info("에이전트를 실행 중입니다... 잠시만 기다려주세요.")

    llm = LLMClient(model="gpt-4-turbo")
    coordinator = Coordinator(llm)

    result = coordinator.run({
        "symbol": symbol,
        "document": document,
        "price_data": price_data,
        "portfolio": {
            "cash": cash,
            "positions": positions
        }
    })

    st.session_state["pipeline_result"] = result  # ✅ 저장

    # 출력
    st.success("에이전트 실행 완료!")

    st.subheader("🧠 Researcher 요약")

    summary_text = result["research"]["summary"]

    # 1. 섹션별로 파싱
    sections = {
        "Key Findings": "",
        "Risks": "",
        "Opportunities": ""
    }

    st.text(result["research"]["summary"])

    matches = re.split(r"###\s+", summary_text)
    for section in matches:
        if section.startswith("Key Findings"):
            sections["Key Findings"] = section.replace("Key Findings:", "").strip()
        elif section.startswith("Risks"):
            sections["Risks"] = section.replace("Risks:", "").strip()
        elif section.startswith("Opportunities"):
            sections["Opportunities"] = section.replace("Opportunities:", "").strip()

    # 2. 요약 출력
    for title, content in sections.items():
        st.markdown(f"**🔹 {title}**")
        st.markdown(content if content else "_No data available_")
        st.markdown("---")

    # 3. 뉴스 출처 출력
    with st.expander("🔍 Sources"):
        for i, src in enumerate(result["research"].get("sources", [])):
            st.markdown(f"**{i + 1}.** {src.splitlines()[0]}")
            st.markdown("> " + src.splitlines()[1] if len(src.splitlines()) > 1 else "")
            st.markdown("")

    # 4. 다운로드 버튼
    download_text = (
        f"# Investment Summary for {result['symbol']}\n\n"
        f"## Key Findings\n{sections['Key Findings']}\n\n"
        f"## Risks\n{sections['Risks']}\n\n"
        f"## Opportunities\n{sections['Opportunities']}"
    )

    st.download_button(
        label="📥 Download Research Report",
        data=download_text,
        file_name=f"{result['symbol']}_summary.md",
        mime="text/markdown"
    )

    st.subheader("📊 Analyst 분석")
    st.markdown(result["analysis"]["technical_analysis"])
    st.json(result["analysis"]["indicators"])

    st.subheader("💡 Trader 판단")
    st.write(f"**결정:** {result['trader']['decision']}")
    st.markdown(result["trader"]["reason"])

    st.subheader("⚠️ Risk Manager")
    st.markdown(result["risk_review"]["review"])
    st.write(f"**승인 여부:** {result['risk_review']['approved']}")

    st.subheader("💼 거래 후 포트폴리오")
    st.json(result["final_portfolio"])
