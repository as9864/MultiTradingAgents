import streamlit as st
from llm.llm_client import LLMClient
from coordinator.mcp_coordinator import MCPCoordinator
from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.trader_agent import TraderAgent
from agents.risk_manager_agent import RiskManagerAgent
from agents import researcher_agent, analyst_agent, trader_agent, risk_manager_agent
from protocol.router import MessageRouter
import pprint

# 💡 Streamlit 설정
st.set_page_config(page_title="AgentTrader MCP", layout="wide")
st.title("🧠 AgentTrader MCP 기반 AI 투자 분석기")

# ✅ 입력 UI
symbol = st.text_input("🔍 분석할 종목코드 (예: AAPL, TSLA)", value="AAPL")

# ✅ 실행 상태 기억
if "mcp_result" not in st.session_state:
    st.session_state["mcp_result"] = None

# ✅ 분석 실행 버튼
if st.button("🚀 MCP 기반 분석 실행"):
    with st.spinner("🧠 에이전트 협업 중..."):

        # MCP 기반 에이전트 구성
        llm = LLMClient()
        router = MessageRouter({
            "Researcher": ResearcherAgent(llm),
            "Analyst": AnalystAgent(llm),
            "Trader": TraderAgent(llm),
            "RiskManager": RiskManagerAgent(llm),
        })

        coordinator = MCPCoordinator(router)
        result = coordinator.run(symbol=symbol)
        st.session_state["mcp_result"] = result

# ✅ 결과 표시
result = st.session_state.get("mcp_result")
if result:
    st.success("✅ 분석 완료!")

    st.header("📚 Research Summary")
    st.markdown(result["research"]["summary"])

    st.header("📈 Analyst Insight")
    st.markdown(result["analysis"]["technical_analysis"])
    st.json(result["analysis"]["indicators"])

    st.header("💡 Trader Decision")
    st.markdown(result["trader"]["decision"])

    st.header("🔐 Risk Review")
    st.markdown(result["risk_review"]["review"])
    st.markdown(f"**Approved:** `{result['risk_review']['approved']}`")

    st.header("💰 Final Portfolio")
    st.json(result["final_portfolio"])

    # 다운로드 버튼
    report_md = f"""
# MCP Investment Summary: {symbol}

## 📚 Research Summary
{result['research']['summary']}

## 📈 Indicators
{result['analysis']['indicators']}

## 📊 Analyst
{result['analysis']['technical_analysis']}

## 💡 Trader Decision
{result['trader']['decision']}

## 🔐 Risk Review
{result['risk_review']['review']}

## 💰 Final Portfolio
{result['final_portfolio']}
"""
    st.download_button("📥 분석 결과 다운로드 (.md)", report_md, file_name=f"{symbol}_summary.md")
