import streamlit as st
from infoharvester.orchestrator.gather_runner import run_full_pipeline
from coordinator.coordinator import Coordinator
from llm.llm_client import LLMClient
from utils.translator import translate_text

st.set_page_config(page_title="AgentTrader", layout="wide")
st.title("📊 AI 주식 분석 시스템 (AgentTrader)")
lang = st.selectbox("🌐 언어 선택 / Language", ["English", "한국어"])
st.header("💡 트레이더 판단 결과" if lang == "한국어" else "💡 Trader Decision")



symbol = st.text_input("분석할 종목 코드 입력 (예: AAPL, TSLA)", value="AAPL")

target_lang = "ko" if lang == "한국어" else "en"

# ✅ 결과 상태 초기화
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if st.button("🚀 분석 실행"):
    with st.spinner("📡 데이터 수집 중..."):
        run_full_pipeline(symbol)

    with st.spinner("🧠 에이전트 판단 중..."):
        llm = LLMClient()
        coordinator = Coordinator(llm)
        result = coordinator.run({"symbol": symbol, "portfolio": {"cash": 10000}})
        st.session_state["analysis_result"] = result
        st.success("✅ 분석 완료!")

# ✅ 이전 실행 결과 불러오기
result = st.session_state.get("analysis_result")
if result:
    st.header("📚 Research Summary")
    research_result = result["research"]["summary"]
    translated_research= translate_text(research_result)
    st.markdown(translated_research)

    st.header("📈 Analyst Insight")
    st.markdown(result["analysis"]["technical_analysis"])
    st.json(result["analysis"]["indicators"])

    st.header("💡 Trader Decision")
    st.markdown(result["trader"]["decision"])

    st.header("🔐 Risk Review")
    st.markdown(result["risk_review"]["review"])
    st.markdown(f"**Approved:** `{result['risk_review']['approved']}`")

    st.header("💰 Updated Portfolio")
    st.json(result["final_portfolio"])

    report_md = f"""
# Investment Summary: {symbol}

## Research Summary
{result['research']['summary']}

## Technical Indicators
{result['analysis']['indicators']}

## Analyst Summary
{result['analysis']['technical_analysis']}

## Trader Decision
{result['trader']['decision']}

## Risk Review
{result['risk_review']['review']}

## Portfolio After Trade
{result['final_portfolio']}
"""
    st.download_button("📥 리포트 다운로드 (.md)", data=report_md, file_name=f"{symbol}_summary.md", mime="text/markdown")