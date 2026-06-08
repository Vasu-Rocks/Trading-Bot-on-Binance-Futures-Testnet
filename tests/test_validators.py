import pytest
from bot.validators import format_value_to_step, validate_and_format_order

def test_format_value_to_step():
    """
    Test Case - The Truncation Engine: Ensure a messy raw float 
    is perfectly truncated to the stepSize without rounding up.
    """
    messy_float = 1.56789
    step_size = "0.01"
    formatted = format_value_to_step(messy_float, step_size)
    assert formatted == "1.56"

def test_under_minimum_quantity(mock_binance_client):
    """
    Test Case - Under Minimum Quantity: Ensure ValueError is raised 
    when quantity is below minQty.
    """
    with pytest.raises(ValueError, match="is less than minimum required"):
        validate_and_format_order(
            client=mock_binance_client,
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=0.0001,  # Below minQty of 0.001
            price=None
        )

@pytest.mark.parametrize("order_type, input_price, input_qty, expected_pass", [
    ("MARKET", None, 0.5, True),           # Valid market order structure
    ("LIMIT", None, 0.5, False),           # Missing price constraint
    ("MARKET", 50000, 0.5, False),         # Market order carrying a price
    ("STOP_MARKET", 48000, 0.1, True),     # Valid trigger order structure
])
def test_validate_order_matrix(mock_binance_client, order_type, input_price, input_qty, expected_pass):
    """
    Test Case - Cross-Parameter Sanity: Parameterized matrix testing valid 
    and invalid order/price combinations.
    """
    if expected_pass:
        fmt_qty, fmt_price = validate_and_format_order(
            client=mock_binance_client,
            symbol="BTCUSDT",
            side="BUY",
            order_type=order_type,
            quantity=input_qty,
            price=input_price
        )
        assert fmt_qty == "0.500" or fmt_qty == "0.100"
    else:
        with pytest.raises(ValueError):
            validate_and_format_order(
                client=mock_binance_client,
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity=input_qty,
                price=input_price
            )
