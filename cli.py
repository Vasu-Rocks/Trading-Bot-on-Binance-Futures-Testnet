import typer
from enum import Enum
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.client import init_client
from bot.validators import validate_and_format_order
from bot.orders import execute_order

app = typer.Typer(help="Binance Futures Testnet Trading Bot")
console = Console()

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_MARKET = "STOP_MARKET"

@app.command("order")
def place_order(
    symbol: str = typer.Option(..., help="Trading pair symbol, e.g., BTCUSDT"),
    side: Side = typer.Option(..., help="Order side: BUY or SELL"),
    order_type: OrderType = typer.Option(..., "--type", help="Type of order: MARKET, LIMIT, STOP_MARKET"),
    quantity: float = typer.Option(..., help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, help="Price (Required for LIMIT and STOP_MARKET)")
):
    """
    Places an order on Binance Futures Testnet.
    """
    # Step 0: Cross-parameter validation
    if order_type in [OrderType.LIMIT, OrderType.STOP_MARKET] and price is None:
        console.print(Panel("Price must be specified for LIMIT or STOP_MARKET orders.", title="Validation Error", style="bold red"))
        raise typer.Exit(code=1)
        
    if order_type == OrderType.MARKET and price is not None:
        console.print(Panel("Price cannot be applied to a MARKET order.", title="Validation Error", style="bold red"))
        raise typer.Exit(code=1)

    # Extract strings from Enum objects to avoid the Enum Object Trap in the backend
    side_str = side.value
    type_str = order_type.value

    try:
        # Step A: Boot up
        client = init_client()
        
        # Step B: Validate & Format
        fmt_quantity, fmt_price = validate_and_format_order(
            client=client, 
            symbol=symbol, 
            side=side_str, 
            order_type=type_str, 
            quantity=quantity, 
            price=price
        )
        
        # Step C: Execute
        response = execute_order(
            client=client,
            symbol=symbol,
            side=side_str,
            order_type=type_str,
            quantity=fmt_quantity,
            price=fmt_price
        )
        
        # Premium UX with Rich
        console.print(Panel("✅ Order Executed Successfully", style="bold green"))
        
        table = Table(title="Order Response Details", show_header=True, header_style="bold magenta")
        table.add_column("Order ID", style="cyan")
        table.add_column("Symbol", style="yellow")
        table.add_column("Side", style="blue")
        table.add_column("Type", style="green")
        table.add_column("Exec Qty", justify="right")
        table.add_column("Avg Price", justify="right")
        table.add_column("Status", style="bold")
        
        table.add_row(
            str(response.get("orderId")),
            response.get("symbol"),
            response.get("side"),
            response.get("type"),
            response.get("executedQty", "0"),
            response.get("avgPrice", "0"),
            response.get("status")
        )
        
        console.print(table)
        
    except (ValueError, ConnectionError, RuntimeError) as e:
        console.print(Panel(str(e), title="Execution Failed", style="bold red"))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
