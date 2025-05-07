class TradingSimulator:
    """
    TraderAgent의 매수/매도 결정을 포트폴리오에 반영하는 거래 시뮬레이터
    """

    def execute_trade(self, symbol: str, action: str, price: float, quantity: int, portfolio: dict) -> dict:
        portfolio = portfolio.copy()
        cash = portfolio.get("cash", 0.0)
        positions = portfolio.get("positions", {}).copy()

        if action == "BUY":
            total_cost = price * quantity
            if cash < total_cost:
                return {"error": "Insufficient cash for trade"}

            if symbol in positions:
                pos = positions[symbol]
                new_qty = pos["quantity"] + quantity
                new_avg = ((pos["quantity"] * pos["avg_price"]) + total_cost) / new_qty
                positions[symbol] = {"quantity": new_qty, "avg_price": round(new_avg, 2)}
            else:
                positions[symbol] = {"quantity": quantity, "avg_price": price}

            cash -= total_cost
            log = f"BUY {quantity} {symbol} @ {price}. New avg price: {positions[symbol]['avg_price']}"

        elif action == "SELL":
            if symbol not in positions or positions[symbol]["quantity"] < quantity:
                return {"error": "Insufficient shares to sell"}

            proceeds = price * quantity
            positions[symbol]["quantity"] -= quantity
            if positions[symbol]["quantity"] == 0:
                del positions[symbol]

            cash += proceeds
            log = f"SELL {quantity} {symbol} @ {price}. Cash after trade: {round(cash, 2)}"

        else:
            return {"error": f"Invalid action: {action}"}

        return {
            "updated_portfolio": {
                "cash": round(cash, 2),
                "positions": positions
            },
            "log": log
        }
