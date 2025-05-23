import schedule
import time
import yaml
from auto_trading.auto_run import run_analysis
# from slack_notifier import send_slack_message
from auto_trading.result_logger import save_result


def load_config(path="auto_trading/trading_config.yml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
symbols = config.get("symbols", ["AAPL"])
run_time = config.get("run_time", "10:00")
slack_enabled = config.get("slack_enabled", True)

def job():
    for symbol in symbols:
        result = run_analysis(symbol)
        message = (
            f"📊 {symbol} 분석 결과\n"
            f"📈 판단: {result['trader']['decision']}\n"
            f"🔐 승인: {'✅' if result['risk_review']['approved'] else '❌'}\n"
            f"💰 포트폴리오: {result['final_portfolio']}"
        )

        print("\n✅ 자동 분석 결과:\n", message)

        save_result(result)  # 📌 CSV 저장 추가

        # if slack_enabled:
            # send_slack_message(message)

# 스케줄 등록
schedule.every().day.at(run_time).do(job)
print(f"⏱ 자동 분석 스케줄 시작됨... (매일 {run_time} / 종목: {', '.join(symbols)})")

while True:
    schedule.run_pending()
    time.sleep(60)