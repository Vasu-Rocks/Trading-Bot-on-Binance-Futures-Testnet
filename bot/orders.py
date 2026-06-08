from binance.client import Client
from binance.exceptions import BinanceAPIException
from .logging_config import logger

def execute_order(client: Client, symbol: str, side: str, order_type: str, quantity: str, price: str = None) -> dict:
    """
    Constructs and fires the order payload to Binance Futures Testnet.
    Expects strictly formatted string values for quantity and price.
    """
    payload = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }
    
    if payload["type"] == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"
    elif payload["type"] == "STOP_MARKET":
        payload["stopPrice"] = price
        
    logger.debug(f"Dispatching order payload: {payload}")
    
    try:
        response = client.futures_create_order(**payload)
        logger.debug(f"Raw Order Response: {response}")
        return response
    except BinanceAPIException as e:
        logger.error(f"Binance API Rejected Order: {e.message} (Code: {e.code}) | Payload: {payload}")
        # Raise a clean exception for the CLI layer to catch
        raise RuntimeError(f"Order rejected by exchange: {e.message}")
    except Exception as e:
        logger.error(f"Network/System error during order execution: {str(e)} | Payload: {payload}")
        raise RuntimeError("Failed to send order due to network or system error.")
