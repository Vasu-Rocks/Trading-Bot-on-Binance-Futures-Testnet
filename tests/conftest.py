import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_binance_client(mocker):
    """
    Creates a MagicMock representation of the Binance Client.
    Pre-packages common responses to prevent real network calls.
    """
    # Mock the Client class
    mock_client_class = mocker.patch('bot.client.Client')
    mock_client_instance = mock_client_class.return_value
    
    # Pre-program futures_ping to return None (Success)
    mock_client_instance.futures_ping.return_value = {}
    
    # Pre-program futures_exchange_info to return a controlled dictionary
    mock_client_instance.futures_exchange_info.return_value = {
        "symbols": [
            {
                "symbol": "BTCUSDT",
                "filters": [
                    {"filterType": "PRICE_FILTER", "tickSize": "0.10"},
                    {"filterType": "LOT_SIZE", "stepSize": "0.001", "minQty": "0.001"}
                ]
            }
        ]
    }
    
    return mock_client_instance
