from infoharvester.market.yahoo_finance import fetch_price_history  # 시세 수집기에서 가격 가져오기

def evaluate_portfolio(portfolio: dict) -> dict:
    """
    현재 포트폴리오에서 자산 평가 총합 및 종목별 가치 계산
    """
    total_value = 0.0
    per_asset = {}

    for symbol, qty in portfolio.items():
        if symbol == "cash":
            per_asset["cash"] = qty
            total_value += qty
        else:
            price = fetch_price_history(symbol)
            value = price * qty
            per_asset[symbol] = value
            total_value += value

    return {
        "total_value": total_value,
        "per_asset": per_asset
    }


def can_allocate(symbol: str, price: float, quantity: int, portfolio_eval: dict, max_weight: float = 0.2) -> bool:
    """
    주어진 매수 판단이 자산 배분 기준을 초과하지 않는지 판단
    """
    total_value = portfolio_eval["total_value"]
    current_value = portfolio_eval["per_asset"].get(symbol, 0.0)

    projected = current_value + (price * quantity)
    weight = projected / total_value

    return weight <= max_weight