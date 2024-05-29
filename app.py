from meta_trader import *
# Load configuration from file
with open("config.json", "r", encoding="utf8") as f:
    config = loads(f.read())
account_id = config["account_id"]
password = config["password"]
server = config["server"]

# Initialize and login
if login_and_initialize(account_id, password, server):
    while True:
        command = input("Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, o: opinning position, q: quit): ")
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
            sl = float(parts[3]) if len(parts) > 3 else 0.00
            tp = float(parts[4]) if len(parts) > 4 else 0.00
            price = float(parts[5]) if len(parts) > 5 else 0.00
            send_order(order_type, symbol, volume, sl, tp, price)
        elif command == "c":
            close_all()
        elif command == "cb":
            close_all("b")
        elif command == "cs":
            close_all("s")
        elif command == "o":
            get_open()
        elif command.startswith("g "):
            parts = command.split()
            row = int(parts[1])
            tf = int(parts[2]) if len(parts) > 2 else mt5.TIMEFRAME_M30
            symbol = parts[3].upper() if len(parts) > 3 else "XAUUSD"
            get_chart_data(symbol, row, tf)
        elif command == "q":
            break
    mt5.shutdown()
else:
    print("Failed to initialize or login to MetaTrader 5")