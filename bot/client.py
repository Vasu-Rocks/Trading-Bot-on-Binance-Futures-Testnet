import os
import sys
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import logger

def init_client() -> Client:
    """
    Initializes the Binance Futures Testnet client and performs a health check.
    """
    load_dotenv()
    
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    
    # Note: BINANCE_BASE_URL is stored in .env as an explicit reference for documentation.
    # However, passing testnet=True below natively handles the internal base URL routing in python-binance.
    
    if not api_key or not api_secret:
        logger.error("API keys missing from .env")
        raise ValueError("API credentials not found. Please check your .env file.")
        
    try:
        # Initialize client with testnet routing enabled
        client = Client(api_key, api_secret, testnet=True)
        
        # Health Check (Ping)
        client.futures_ping()
        logger.debug("Successfully pinged Binance Futures Testnet.")
        return client
    except BinanceAPIException as e:
        logger.error(f"Binance API error during health check: {e.message} (Code: {e.code})")
        raise ConnectionError("Failed to connect to Binance Testnet API. Please verify your keys and network.")
    except (BinanceRequestException, Exception) as e:
        logger.error(f"Network or system error during health check: {str(e)}")
        raise ConnectionError("Failed to connect to Binance Testnet. Please check your internet connection.")
