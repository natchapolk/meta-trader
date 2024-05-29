from datetime import datetime
from json import loads
import MetaTrader5 as mt5
import pandas as pd
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
def send_order(order_type: str, symbol: str, volume: float = 0.1, sl: float = 0.00, tp: float = 0.00, price: float = 0.00) -> bool:
    # Check if the symbol is available in MarketWatch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}")
        print("Error Code:", mt5.last_error())
        return False

    # Determine the order type and price
    if price != 0.00:
        action = mt5.TRADE_ACTION_DEAL
        type = mt5.ORDER_TYPE_BUY if order_type == "b" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).ask if order_type == "b" else mt5.symbol_info_tick(symbol).bid
    else:
        action = mt5.TRADE_ACTION_PENDING
        type = mt5.ORDER_TYPE_BUY_LIMIT if order_type == "b" else mt5.ORDER_TYPE_SELL_LIMIT

    # Adjust stop-loss and take-profit levels based on order type
    if sl != 0.0:
        sl = price - sl if order_type == "b" else price + sl
    if tp != 0.0:
        tp = price + tp if order_type == "b" else price - tp

    # Create an order request
    request = {
        "action": action,
        "symbol": symbol,
        "volume": volume,
        "type": type,
        "price": price,
        "sl": sl,
        "tp": tp,
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
    print(price)
    return True

# Function to close all open positions
def close_all(type: str = "") -> None:
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
        # if type is buy or sell continue
        if (type == "b" and order_type == mt5.ORDER_TYPE_SELL) or (type == "s" and order_type == mt5.ORDER_TYPE_BUY):
            continue
        # Determine the opposite action to close the position
        action = mt5.ORDER_TYPE_SELL if order_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if action == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask

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
            print(f"Position #{ticket} closed successfully at{price} ")

# Function to get all open ticket
def get_open() -> None:
    # Get open positions
    positions = mt5.positions_get()
    if positions is None:
        print("No positions found, error code:", mt5.last_error())
        return

    # get data for each position
    for position in positions:
        symbol = position.symbol
        volume = position.volume
        price_open = position.price_open
        sl = position.sl
        tp = position.tp
        print(f"{volume} {symbol} at  {price_open} with sl = {sl} and tp = {tp}")

# Retrieves chart data from MetaTrader 5.
def get_chart_data(symbol, rows, timeframe):
    # Get the historical data
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, rows)
    # Check if data is retrieved successfully
    if rates is None:
        print(f"Failed to retrieve data for {symbol}")
        return None
    
    # Convert to DataFrame for better handling
    df = pd.DataFrame(rates)
    
    # Convert 'time' from timestamp to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df)
    return df
    
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