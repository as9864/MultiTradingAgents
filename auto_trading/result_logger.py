import csv
import os
from datetime import datetime

CSV_FILE = "auto_trading/results/results.csv"

def save_result(result: dict):
    # 결과에서 필요한 정보 추출
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    symbol = result["symbol"]
    decision = result["trader"]["decision"]
    approved = "✅" if result["risk_review"]["approved"] else "❌"
    price = result.get("risk_review", {}).get("price", "-")
    portfolio = result.get("final_portfolio", {})
    quantity = portfolio.get(symbol, 0)
    cash = portfolio.get("cash", "-")

    row = [now, symbol, decision, approved, price, quantity, cash, str(portfolio)]

    # 파일이 없으면 헤더 먼저 작성
    write_header = not os.path.exists(CSV_FILE)

    with open(CSV_FILE, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["날짜", "종목", "판단", "승인", "가격", "보유수량", "현금", "전체포트폴리오"])
        writer.writerow(row)

    print(f"📝 CSV 저장 완료: {symbol} ({decision}, {approved})")