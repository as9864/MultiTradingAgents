import streamlit as st
from llm.llm_client import LLMClient
from coordinator.mcp_coordinator import MCPCoordinator
from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent
from agents.trader_agent import TraderAgent
from agents.risk_manager_agent import RiskManagerAgent
from agents.execution_agent import ExecutionAgent
from protocol.router import MessageRouter
import pandas as pd
import os
import json

import requests

# ✅ Streamlit 설정
st.set_page_config(page_title="AgentTrader MCP", layout="wide")
st.title("🧠 AgentTrader + AgentExecutor 통합 대시보드")

# ✅ 종목 입력
symbol = st.text_input("🔍 분석할 종목코드 (예: AAPL)", value="AAPL")

# ✅ 세션 상태 초기화
if "mcp_result" not in st.session_state:
    st.session_state["mcp_result"] = None


# ✅ 분석 실행 버튼
if st.button("🚀 MCP 기반 분석 실행"):
    with st.spinner("에이전트 협업 중..."):
        # router 생성 전에 모든 에이전트를 만든다
        llm = LLMClient()
        researcher = ResearcherAgent(llm)
        analyst = AnalystAgent(llm)
        risk_manager = RiskManagerAgent(llm)
        execution = ExecutionAgent()

        # Trader는 router가 필요하므로 가장 마지막
        router = MessageRouter({})
        trader = TraderAgent(llm, router)

        # 이제 등록
        router.agents = {
            "Researcher": researcher,
            "Analyst": analyst,
            "Trader": trader,
            "RiskManager": risk_manager,
            "ExecutionAgent": execution
        }

        # MCP 구성
        # llm = LLMClient()
        # router = MessageRouter({
        #     "Researcher": ResearcherAgent(llm),
        #     "Analyst": AnalystAgent(llm),
        #     "Trader": TraderAgent(llm,router),
        #     "RiskManager": RiskManagerAgent(llm),  # ✅ 꼭 있어야 함
        #     "ExecutionAgent": ExecutionAgent()
        # })

        coordinator = MCPCoordinator(router)
        result = coordinator.run(symbol=symbol)
        st.session_state["mcp_result"] = result

# ✅ 결과 표시
result = st.session_state["mcp_result"]
if result:
    st.success("✅ 분석 완료")

    st.header("📚 Research Summary")
    st.markdown(result["research"]["summary"])

    st.header("📈 Analyst Insight")
    st.markdown(result["analysis"]["technical_analysis"])
    st.json(result["analysis"]["indicators"])

    st.header("💡 Trader Decision")
    st.markdown(f"**판단:** `{result['trader']['decision']}`")
    st.markdown(result["trader"]["reason"])

    st.header("🔐 Risk Review")
    st.markdown(result["risk_review"]["review"])
    st.markdown(f"**승인:** `{result['risk_review']['approved']}`")

    st.header("💰 Final Portfolio")
    st.json(result["final_portfolio"])

    # 📥 분석 결과 다운로드
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

    # ✅ AgentExecutor 실행 로그 추가
    st.header("📊 AgentExecutor 주문 실행 로그")

    def load_execution_log():

        df_log = pd.DataFrame(requests.get("http://localhost:8000/api/logs").json())
        return df_log

    df_log = load_execution_log()

    if df_log.empty:
        st.warning("실행 로그가 없습니다.")
    else:
        df_filtered = df_log[df_log["symbol"] == symbol.upper()]

        if df_filtered.empty:
            st.info(f"{symbol} 종목에 대한 실행 기록 없음")
        else:
            st.subheader("📄 실행 내역 테이블")
            st.dataframe(df_filtered)

            st.subheader("📈 평균 체결가 추이")
            chart_data = df_filtered[["timestamp", "avg_price"]].set_index("timestamp")
            st.line_chart(chart_data.rename(columns={"avg_price": "평균 체결가"}))