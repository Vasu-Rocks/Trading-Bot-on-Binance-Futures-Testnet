import pytest
from binance.exceptions import BinanceAPIException
from bot.client import init_client

def test_init_client_success(mock_binance_client, monkeypatch):
    """
    Test Case - Happy Path: Ensure the client initializes successfully
    when keys are present and the network ping succeeds.
    """
    # Simulate valid environment variables
    monkeypatch.setenv("BINANCE_TESTNET_API_KEY", "test_key")
    monkeypatch.setenv("BINANCE_TESTNET_API_SECRET", "test_secret")
    
    # mock_binance_client fixture already mocks futures_ping to succeed
    client = init_client()
    
    # Assert client is returned and futures_ping was called
    assert client is not None
    client.futures_ping.assert_called_once()

def test_init_client_missing_keys(mocker, monkeypatch):
    """
    Test Case - Missing Keys: Ensure init_client raises a ValueError
    when API keys are missing from the environment.
    """
    # CRITICAL: Mock load_dotenv so it becomes a harmless no-op.
    # This prevents it from reloading keys from the local .env file.
    mocker.patch('bot.client.load_dotenv')
    
    # Completely clear out the API key from the environment
    monkeypatch.delenv("BINANCE_TESTNET_API_KEY", raising=False)
    monkeypatch.delenv("BINANCE_TESTNET_API_SECRET", raising=False)
    
    with pytest.raises(ValueError, match="API credentials not found"):
        init_client()

def test_init_client_network_failure(mock_binance_client, monkeypatch):
    """
    Test Case - API Network Failure: Ensure BinanceAPIException during
    ping is intercepted and sanitized into a ConnectionError.
    """
    monkeypatch.setenv("BINANCE_TESTNET_API_KEY", "test_key")
    monkeypatch.setenv("BINANCE_TESTNET_API_SECRET", "test_secret")
    
    # Force futures_ping to raise a BinanceAPIException
    class MockResponse:
        status_code = 401
        text = '{"code": -2015, "msg": "Invalid API-key, IP, or permissions"}'
    
    mock_binance_client.futures_ping.side_effect = BinanceAPIException(
        MockResponse(), status_code=401, text=MockResponse.text
    )
    
    with pytest.raises(ConnectionError, match="Failed to connect to Binance Testnet API"):
        init_client()
