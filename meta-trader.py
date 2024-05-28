import MetaTrader5 as mt5
from json import loads
from typing import Optional, Tuple

# Function to login and initialize MetaTrader 5
def login_and_initialize(account_id: int, password: str, server: str) -> bool:
    if not mt5.initialize():
        print("Failed to initialize MetaTrader 5")
        print("Error Code:", mt5.last_error())
        return False
    print("MetaTrader 5 initialized successfully")
    if not mt5.login(account_id, password=password, server=server):
        print("Failed to login to account")
        print("Error Code:", mt5.last_error())
        mt5.shutdown()
        return False
    print("Logged in to account successfully")
    return True

# Function to send order to MetaTrader 5
def send_order(order_type: str, symbol: str, volume: float = 0.1, price: float = 0.0) -> bool:
    # Check if the symbol is available in MarketWatch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        print("Error Code:", mt5.last_error())
        return False

    # Determine the order type and price
    action = mt5.ORDER_TYPE_BUY if order_type == "b" else mt5.ORDER_TYPE_SELL
    if price == 0.0:
        price = mt5.symbol_info_tick(symbol).ask if order_type == "b" else mt5.symbol_info_tick(symbol).bid

    # Create an order request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": action,
        "price": price,
        "deviation": 20,
        "magic": 234000,
        "comment": f"send order for {symbol}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send the request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order send failed, retcode={result.retcode}")
        print("Error Code:", mt5.last_error())
        return False
    print("Order executed successfully")
    return True

# Function to close all open positions
def close_all() -> None:
    # Get open positions
    positions = mt5.positions_get()
    if positions is None:
        print("No positions found, error code:", mt5.last_error())
        return

    # Close each position
    for position in positions:
        symbol = position.symbol
        ticket = position.ticket
        volume = position.volume
        order_type = position.type

        # Determine the opposite action to close the position
        action = mt5.ORDER_TYPE_SELL if order_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if action == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask

        # Create request to close position
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": action,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "Close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        # Send the request to close position
        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to close position #{ticket}, error code: {result.retcode}")
        else:
            print(f"Position #{ticket} closed successfully")

# Function to check current account balance
def check_balance() -> Optional[Tuple[float, float]]:
    account_info = mt5.account_info()
    if account_info is None:
        print("Failed to get account info")
        print("Error Code:", mt5.last_error())
        return None
    print(f"Balance: {account_info.balance}, Equity: {account_info.equity}")
    return account_info.balance, account_info.equity

# Function to get market data for a given symbol
def get_market_data(symbol: str) -> Optional[mt5.Tick]:
    # Ensure the symbol is available in MarketWatch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        print("Error Code:", mt5.last_error())
        return None

    # Get tick data
    tick_info = mt5.symbol_info_tick(symbol)
    if tick_info is None:
        print(f"Failed to get tick info for {symbol}")
        print("Error Code:", mt5.last_error())
        return None

    print(f"{symbol} Ask: {tick_info.ask}, Bid: {tick_info.bid}")
    return tick_info

# Load configuration from file
with open("config.json", "r", encoding="utf8") as f:
    config = loads(f.read())
account_id = config["account_id"]
password = config["password"]
server = config["server"]

# Initialize and login
if login_and_initialize(account_id, password, server):
    while True:
        command = input("Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, q: quit): ")
        if command == "a":
            check_balance()
        elif command == "p":
            get_market_data("XAUUSD")
        elif command.startswith("p "):
            get_market_data(command.split()[1].upper())
        elif command == "b" or command == "s":
            send_order(command, "XAUUSD", 0.1, 0.00)
        elif command.startswith("b ") or command.startswith("s "):
            parts = command.split()
            order_type = parts[0].lower()
            volume = float(parts[1])
            symbol = parts[2].upper() if len(parts) > 2 else "XAUUSD"
            price = float(parts[3]) if len(parts) > 3 else 0.0
            send_order(order_type, symbol, volume, price)
        elif command == "c":
            close_all()
        elif command == "q":
            break
    mt5.shutdown()
else:
    print("Failed to initialize or login to MetaTrader 5")