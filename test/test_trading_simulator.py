from simulator.trading_simulator import TradingSimulator


def test_trading():
    simulator = TradingSimulator()

    # 초기 포트폴리오
    portfolio = {
        "cash": 10000,
        "positions": {
            "AAPL": {"quantity": 20, "avg_price": 150.0}
        }
    }

    # 매수 테스트
    result_buy = simulator.execute_trade(
        symbol="AAPL",
        action="BUY",
        price=160.0,
        quantity=10,
        portfolio=portfolio
    )

    print("\n💰 BUY Trade Result:")
    print(result_buy)

    # 매도 테스트
    updated_portfolio = result_buy.get("updated_portfolio", portfolio)
    result_sell = simulator.execute_trade(
        symbol="AAPL",
        action="SELL",
        price=165.0,
        quantity=15,
        portfolio=updated_portfolio
    )

    print("\n💵 SELL Trade Result:")
    print(result_sell)


if __name__ == "__main__":
    test_trading()
