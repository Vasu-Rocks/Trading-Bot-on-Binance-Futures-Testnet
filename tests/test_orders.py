import pytest
from binance.exceptions import BinanceAPIException
from bot.orders import execute_order

def test_execute_limit_order(mock_binance_client):
    """
    Test Case - Limit Formatting Enforcement: Ensure LIMIT orders 
    explicitly append timeInForce="GTC".
    """
    execute_order(
        client=mock_binance_client,
        symbol="BTCUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity="0.500",
        price="50000.00"
    )
    
    mock_binance_client.futures_create_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="SELL",
        type="LIMIT",
        quantity="0.500",
        price="50000.00",
        timeInForce="GTC"
    )

def test_execute_stop_market_order(mock_binance_client):
    """
    Test Case - Stop Market Routing: Ensure STOP_MARKET orders map 
    price to stopPrice instead of price.
    """
    execute_order(
        client=mock_binance_client,
        symbol="BTCUSDT",
        side="SELL",
        order_type="STOP_MARKET",
        quantity="0.100",
        price="48000.00"
    )
    
    mock_binance_client.futures_create_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="SELL",
        type="STOP_MARKET",
        quantity="0.100",
        stopPrice="48000.00"
    )

def test_execute_order_exception_sanitization(mock_binance_client):
    """
    Test Case - Exception Sanitization: Ensure raw BinanceAPIExceptions 
    are intercepted and re-raised as clean RuntimeErrors.
    """
    class MockResponse:
        status_code = 400
        text = '{"code": -2019, "msg": "Margin is insufficient."}'
        
    mock_binance_client.futures_create_order.side_effect = BinanceAPIException(
        MockResponse(), status_code=400, text=MockResponse.text
    )
    
    with pytest.raises(RuntimeError, match="Order rejected by exchange: Margin is insufficient."):
        execute_order(
            client=mock_binance_client,
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.500"
        )
