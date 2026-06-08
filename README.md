# Binance Futures Testnet Trading Bot

A highly defensive Command Line Interface (CLI) trading bot engineered to validate and execute leveraged futures orders on the Binance Futures Testnet API. Built with Python, modern type hinting, and automated deterministic mocking.

## Key Features

* **Typer Orchestration:** Modern, interactive CLI handling with strict automated input validation using native Python Enums.
* **Premium Terminal UX:** Rich terminal panels for errors and color-coded structural data tables for successful order execution receipts using `rich`.
* **Airtight Precision Engine:** Custom `Decimal` truncation mechanism built into the validator layer to completely eliminate floating-point precision issues (`LOT_SIZE` and `PRICE_FILTER`).
* **Performance Optimizations:** Module-level caching for exchange rules (`futures_exchange_info`) to maintain a sub-second runtime footprint and prevent API rate-limiting.
* **100% Isolated Test Suite:** Comprehensive unit testing using `pytest` and `pytest-mock` to completely decouple the test matrix from live internet or local filesystem states.

---

## Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone and Navigate
```bash
git clone https://github.com/yourusername/binance-futures-bot.git
cd binance-futures-bot
```

### 3. Establish Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate on Windows (CMD):
venv\Scripts\activate.bat
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Configuration

The application requires secure authentication credentials for the Binance Futures Testnet.

Open `.env` and populate it with your personal Testnet API keys:
```env
BINANCE_TESTNET_API_KEY=your_actual_testnet_api_key_here
BINANCE_TESTNET_API_SECRET=your_actual_testnet_api_secret_here
```

> [!WARNING]
> The `.env` file contains private credentials. It is explicitly ignored via `.gitignore` and must never be committed to source control.

---

## CLI Work

The bot hoists commands directly to the root execution level for maximum efficiency.

### Global Help Menu
To inspect available options, parameters, and global constraints:
```bash
python cli.py --help
```

### 1. Execute a Market Order
Market orders execute immediately at the current market price. Passing a `--price` parameter to a `MARKET` order will trigger an instant pre-flight rejection.
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.5
```

### 2. Execute a Limit Order
Limit orders require a valid constraint price. If the `--price` parameter is missing, the application will fail-fast before hitting the network.
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.25 --price 62500.00
```

### 3. Execute a Stop Market Order
Stop Market orders require a trigger price passed directly via the `--price` parameter, which the routing engine automatically maps to Binance's native `stopPrice` parameter.
```bash
python cli.py --symbol ETHUSDT --side BUY --type STOP_MARKET --quantity 1.0 --price 3450.00
```

### Parameter Reference Matrix

| Option | Type | Required | Allowed Choices / Formatting | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--symbol` | `STR` | Yes | e.g., `BTCUSDT`, `ETHUSDT` | Target trading pair asset ticker. |
| `--side` | `ENUM` | Yes | `BUY`, `SELL` | Order direction. Automatically validated. |
| `--type` | `ENUM` | Yes | `MARKET`, `LIMIT`, `STOP_MARKET` | Execution type strategy rules. |
| `--quantity` | `FLOAT` | Yes | Any positive float | Raw size to trade. Truncated to `stepSize`. |
| `--price` | `FLOAT` | Optional | Required for `LIMIT`/`STOP_MARKET` | Execution target or trigger target price. |

---

## Running the Test Suite

The automated test suite runs completely hermetically—meaning it simulates all exchange API interaction states dynamically via fixtures. You do not need active API keys or an internet connection to run tests.

To run the complete test suite with detailed verbose outputs:
```bash
python -m pytest -v
```

### Test Suite Map

* **`tests/test_client.py`:** Verifies credential presence verification, happy-path connection routing, and third-party network failure wrapping.
* **`tests/test_validators.py`:** Validates sub-minimum volume rejections, exact decimal truncation constraints, and cross-parameter dependency tables.
* **`tests/test_orders.py`:** Asserts API structural grammar compliance, Limit-order timing parameter attachments, and Stop-market payload key re-mappings.

---

## Assumptions Made

1. **Testnet Scope**: We assume the user strictly operates on the Binance Futures Testnet and does not use these keys for the Live exchange.
2. **Terminal Encoding**: We assume modern terminal support for rich table rendering. For older Windows PowerShell versions, we prepend `python -X utf8` to force encoding compatibility.
3. **Module Path**: The CLI assumes it is executed from the root directory so imports like `bot.client` resolve correctly.
4. **Environment File**: The `.env` template is the singular source of truth for credentials.

---

## Validation Commands Executed

The following exact commands were run to successfully validate the live execution against the Testnet API and capture logging telemetry:

**1. Market Buy Validation**
```bash
python -X utf8 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.5
```

**2. Limit Sell Validation**
```bash
python -X utf8 cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.25 --price 62500.00
```

**3. Intentional Failure Validation (Negative Quantity)**
```bash
python -X utf8 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity -0.5
```

---
## Thank You!!

