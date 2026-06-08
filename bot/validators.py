from decimal import Decimal, ROUND_DOWN
from binance.client import Client
from .logging_config import logger

# Module-level cache to prevent sluggish CLI performance and rate limiting
_exchange_info_cache = None

def fetch_exchange_filters(client: Client, symbol: str):
    """
    Fetches the dynamic exchange rules for a given symbol from Binance Futures.
    Returns tick_size, step_size, and min_qty. Caches the response internally.
    """
    global _exchange_info_cache
    if not _exchange_info_cache:
        try:
            logger.debug("Fetching futures exchange info (first time setup)...")
            _exchange_info_cache = client.futures_exchange_info()
        except Exception as e:
            logger.error(f"Failed to fetch exchange info: {e}")
            raise ValueError("Failed to fetch live exchange rules. Please check network.")
            
    exchange_info = _exchange_info_cache
        
    for s in exchange_info['symbols']:
        if s['symbol'] == symbol:
            filters = s['filters']
            tick_size = next((f['tickSize'] for f in filters if f['filterType'] == 'PRICE_FILTER'), None)
            step_size = next((f['stepSize'] for f in filters if f['filterType'] == 'LOT_SIZE'), None)
            min_qty = next((f['minQty'] for f in filters if f['filterType'] == 'LOT_SIZE'), None)
            
            if not tick_size or not step_size or not min_qty:
                logger.error(f"Missing essential filters for {symbol}. Filters: {filters}")
                raise ValueError(f"Could not extract strict trading filters for {symbol}.")
                
            return tick_size, step_size, min_qty
            
    logger.error(f"Symbol {symbol} not found in exchange info.")
    raise ValueError(f"Symbol {symbol} is invalid or not supported on Futures Testnet.")

def format_value_to_step(value: float, step_str: str) -> str:
    """
    Truncates a float value to match the exact decimal precision of the step_str.
    Fixes the 'Float Formatting Trap'.
    Example: value=1.5, step_str="0.001" -> returns "1.500"
    """
    step_dec = Decimal(step_str).normalize()
    val_dec = Decimal(str(value))
    
    # Quantize truncates the float exactly to the precision of the step size
    # ROUND_DOWN ensures we don't accidentally round up into an invalid LOT_SIZE or PRICE_FILTER
    formatted_val = val_dec.quantize(step_dec, rounding=ROUND_DOWN)
    
    # Return as exact string required by Binance
    return "{:f}".format(formatted_val)  # {:f} prevents scientific notation

def validate_and_format_order(client: Client, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Performs pre-flight checks and strictly formats floats against live exchange rules.
    Returns formatted_quantity, formatted_price
    """
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()
    
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
        
    if order_type not in ['MARKET', 'LIMIT', 'STOP_MARKET']:
        raise ValueError(f"Invalid order type: {order_type}.")
        
    if order_type in ['LIMIT', 'STOP_MARKET'] and price is None:
        raise ValueError(f"Price must be provided for {order_type} orders.")
        
    if order_type == 'MARKET' and price is not None:
        raise ValueError("Price cannot be applied to a MARKET order.")
        
    # Fetch rules
    tick_size, step_size, min_qty = fetch_exchange_filters(client, symbol)
    logger.debug(f"[{symbol}] Filters: tickSize={tick_size}, stepSize={step_size}, minQty={min_qty}")
    
    # Validate Quantity consistently using Decimals
    if Decimal(str(quantity)) < Decimal(min_qty):
        raise ValueError(f"Quantity {quantity} is less than minimum required {min_qty} for {symbol}.")
        
    # Format Quantity
    fmt_quantity = format_value_to_step(quantity, step_size)
    
    # Format Price (if applicable)
    fmt_price = None
    if price is not None:
        fmt_price = format_value_to_step(price, tick_size)
        
    logger.debug(f"Formatted input: qty={fmt_quantity}, price={fmt_price}")
    
    return fmt_quantity, fmt_price
