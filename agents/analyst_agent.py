import pandas as pd
# from agents.base_agent import BaseAgent
from llm.llm_client import LLMClient
from infoharvester.market.data_loader import load_price_data
from protocol.agent_base import AgentBase
from protocol.message import Message
from infoharvester.market.yahoo_finance import fetch_price_history
from infoharvester.market.indicator_utils import apply_indicators


class AnalystAgent(AgentBase):
    """
    기술적 지표를 계산하고 이를 해석하도록 LLM에 요청하는 에이전트
    input_data 예시:
    {
        "symbol": "AAPL",
        "price_data": pd.DataFrame
    }
    """

    def __init__(self, llm_client: LLMClient):
        super().__init__("Analyst")
        self.llm = llm_client
        self.system_prompt = self.load_prompt("prompts/analyst.txt")




    def calculate_indicators(self, df: pd.DataFrame) -> dict:
        df = df.copy()
        df["SMA_5"] = df["close"].rolling(window=5).mean()
        df["RSI_14"] = self._calculate_rsi(df["close"], 14)

        return {
            "latest_close": df["close"].iloc[-1],
            "sma_5": df["SMA_5"].iloc[-1],
            "rsi_14": df["RSI_14"].iloc[-1]
        }

    def _calculate_rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def run(self, input_data: dict) -> dict:
        symbol = input_data.get("symbol", "UNKNOWN")
        df = input_data.get("price_data") #기존 price_data 호출 파트 수정
        # df = load_price_data(symbol)

        if df is None or df.empty:
            return {"error": "No price data provided"}

        indicators = self.calculate_indicators(df)

        user_prompt = (
            f"You are analyzing stock data for {symbol}.\n"
            f"The latest closing price is {indicators['latest_close']:.2f}.\n"
            f"The 5-day SMA is {indicators['sma_5']:.2f}.\n"
            f"The 14-day RSI is {indicators['rsi_14']:.2f}.\n"
            f"What is your analysis of this stock? Provide a clear summary."
        )

        analysis = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)

        return {
            "agent": "Analyst",
            "symbol": symbol,
            "technical_analysis": analysis,
            "indicators": indicators,
            "price_data": df
        }

    def handle_message(self, message: Message) -> Message:
        if message.type != "request" or message.content.get("action") != "analyze":
            return Message(
                sender=self.name,
                receiver=message.sender,
                type="error",
                content={"error": "Invalid message type or action"}
            )

        symbol = message.content.get("symbol", "UNKNOWN")

        try:
            df = fetch_price_history(symbol, period="60d")
            df = apply_indicators(df)

            indicators = {
                "latest_close": df["close"].iloc[-1],
                "sma_5": df["SMA_5"].iloc[-1],
                "rsi_14": df["RSI_14"].iloc[-1]
            }

            user_prompt = (
                f"You are analyzing stock data for {symbol}.\n"
                f"The latest closing price is {indicators['latest_close']:.2f}.\n"
                f"The 5-day SMA is {indicators['sma_5']:.2f}.\n"
                f"The 14-day RSI is {indicators['rsi_14']:.2f}.\n"
                f"What is your technical analysis of this stock? Provide a concise interpretation."
            )

            analysis = self.llm.chat(system_prompt=self.system_prompt, user_prompt=user_prompt)

            return Message(
                sender=self.name,
                receiver=message.sender,
                type="response",
                content={
                    "symbol": symbol,
                    "technical_analysis": analysis,
                    "indicators": indicators
                }
            )

        except Exception as e:
            return Message(
                sender=self.name,
                receiver=message.sender,
                type="error",
                content={"error": str(e)}
            )