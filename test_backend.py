import os
import sys
from rich.console import Console

# Ensure Python can find the 'bot' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.client import init_client
from bot.validators import validate_and_format_order
from bot.orders import execute_order

console = Console()

def run_test():
    console.print("[bold cyan]=== Starting Backend Test ===[/bold cyan]")
    
    # Step 1: Initialize Client
    try:
        console.print("\n[yellow]1. Initializing client and pinging testnet...[/yellow]")
        client = init_client()
        console.print("[green]✅ Client initialized and connected successfully.[/green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to initialize client: {e}[/bold red]")
        sys.exit(1)
        
    # Test Parameters
    symbol = "BTCUSDT"
    side = "BUY"
    order_type = "MARKET"
    quantity = 0.005  # A safe, small testnet quantity
    price = None
    
    console.print(f"\n[yellow]2. Validating {order_type} {side} order for {quantity} {symbol}...[/yellow]")
    
    try:
        fmt_quantity, fmt_price = validate_and_format_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        console.print(f"[green]✅ Validation passed! Exact exchange strings -> Qty: '{fmt_quantity}', Price: '{fmt_price}'[/green]")
    except Exception as e:
        console.print(f"[bold red]❌ Validation failed: {e}[/bold red]")
        sys.exit(1)
        
    console.print("\n[yellow]3. Firing Order Payload to Binance Testnet...[/yellow]")
    try:
        response = execute_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=fmt_quantity,
            price=fmt_price
        )
        console.print("[bold green]✅ Order Executed Successfully! Raw Response:[/bold green]")
        console.print(response)
    except Exception as e:
        console.print(f"[bold red]❌ Execution failed: {e}[/bold red]")
        sys.exit(1)
        
    console.print("\n[bold cyan]=== Test Complete! Check trading_bot.log for the audit trail. ===[/bold cyan]")

if __name__ == "__main__":
    run_test()
