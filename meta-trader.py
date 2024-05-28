import MetaTrader5 as mt5
from json import loads

# Function to initialize MetaTrader 5
def initialize_mt5():
    if not mt5.initialize():
        print("Failed to initialize MetaTrader5")
        print("Error Code:", mt5.last_error())
        mt5.shutdown()
        return False
    else:
        print("MetaTrader5 initialized successfully")
        return True

# Function to login to your trading account
def login(account_id, password, server):
    if not mt5.login(account_id, password=password, server=server):
        print("Failed to login to account")
        print("Error Code:", mt5.last_error())
        mt5.shutdown()
        return False
    else:
        print("Logged in to account successfully")
        return True

# Function to buy XAUUSD
def buy_xauusd(volume):
    symbol = "XAUUSD"
    # Check if the symbol is available in MarketWatch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        print("Error Code:", mt5.last_error())
        return False
    
    # Create a buy request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 20,
        "magic": 234000,
        "comment": "Buy XAUUSD",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    print(request)    
    # Send the request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order send failed, retcode={result.retcode}")
        print("Error Code:", mt5.last_error())
        return False
    print("Buy order executed successfully")
    return True

# Function to sell XAUUSD
def sell_xauusd(volume):
    symbol = "XAUUSD"
    # Check if the symbol is available in MarketWatch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        print("Error Code:", mt5.last_error())
        return False
    
    # Create a sell request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).bid,
        "deviation": 20,
        "magic": 234000,
        "comment": "Sell XAUUSD",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    # Send the request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order send failed, retcode={result.retcode}")
        print("Error Code:", mt5.last_error())
        return False
    print("Sell order executed successfully")
    return True

# Function to check current account balance
def check_balance():
    account_info = mt5.account_info()
    if account_info is None:
        print("Failed to get account info")
        print("Error Code:", mt5.last_error())
        return None
    print(f"Balance: {account_info.balance}, Equity: {account_info.equity}")
    return account_info.balance, account_info.equity

# Function to get market data for XAUUSD
def get_xauusd_data():
    symbol = "XAUUSD"
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
    
    print(f"XAUUSD Ask: {tick_info.ask}, Bid: {tick_info.bid}")
    return tick_info

# Function to close all open positions
def close_all():
    # Get open positions
    positions = mt5.positions_get()
    if positions is None:
        print("No positions found, error code: {}".format(mt5.last_error()))
        return

    # Close each position
    for position in positions:
        symbol = position.symbol
        ticket = position.ticket
        volume = position.volume
        order_type = position.type

        # Determine the opposite action to close the position
        if order_type == mt5.ORDER_TYPE_BUY:
            action = mt5.ORDER_TYPE_SELL
        elif order_type == mt5.ORDER_TYPE_SELL:
            action = mt5.ORDER_TYPE_BUY
        else:
            continue

        # Create request to close position
        print(action, mt5.symbol_info_tick(symbol).bid if action == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask)
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": action,
            "position": ticket,
            "price": mt5.symbol_info_tick(symbol).bid if action == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
            "deviation": 20,
            "magic": 234000,
            "comment": "Close position",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
        print(close_request)
        # Send the request to close position
        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Failed to close position #{}, error code: {}".format(ticket, result.retcode))
        else:
            print("Position #{} closed successfully".format(ticket))

# Load configuration from file
with open("config.json", "r", encoding="utf8") as f:
    config = loads(f.read())

account_id = config["account_id"]
password = config["password"]
server = config["server"]

# Initialize and login
if initialize_mt5() and login(account_id, password, server):
    while True:
        command = input("Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, q: quit): ")
        if command == "a":
            check_balance()
        elif command == "p":
            get_xauusd_data()
        elif command == "b":
            buy_xauusd(0.1)  # Example volume
        elif command == "s":
            sell_xauusd(0.1)  # Example volume
        elif command == "c":
            close_all()
        elif command == "q":
            break
    mt5.shutdown()
else:
    print("Failed to initialize or login to MetaTrader 5")
