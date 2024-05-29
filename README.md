# meta-trader
This repository contains Python scripts to interact with MetaTrader 5 using the `MetaTrader5` Python module. The script allows you to login, send orders, retrieve market data, check balance, and more.

## Prerequisites

1. **MetaTrader 5 Platform**: Ensure you have the MetaTrader 5 trading platform installed and running.
2. **MetaTrader5 Python Module**: Install the required modules using pip:
    ```sh
    pip install -r requirements.txt
    ```

## Files

- `meta_trader.py`: Contains functions to interact with MetaTrader 5.
- `app.py`: Command-line application to execute functions defined in `meta_trader.py`.
- `config.json`: Configuration file to store MetaTrader account details.

## Configuration

Create a `config.json` file with the following structure to store your MetaTrader account details:

```json
{
  "account_id": "your_account_id",
  "password": "your_password",
  "server": "your_server"
}
```
## Usage
1. 
Install Dependencies:
```sh
pip install -r requirements.txt
```
2. 
Run the Application:
Ensure MetaTrader 5 is running and connected to a broker account. Then run the application:
```sh
python app.py
```
## Commands
Once the application is running, you can use the following commands:
• `a`: Check account balance.
• `b`: Buy XAUUSD with 0.1 lot.
• `b <volume>`: Buy XAUUSD with specified volume.
• `b <volume> <symbol>`: Buy specified symbol with specified volume.
• `b <volume> <symbol> <sl>`: Buy specified symbol with specified volume and stop-loss.
• `b <volume> <symbol> <sl> <tp>`: Buy specified symbol with specified volume, stop-loss, and take-profit.
• `s`: Sell XAUUSD with 0.1 lot.
• `s <volume>`: Sell XAUUSD with specified volume.
• `s <volume> <symbol>`: Sell specified symbol with specified volume.
• `s <volume> <symbol> <sl>`: Sell specified symbol with specified volume and stop-loss.
• `s <volume> <symbol> <sl> <tp>`: Sell specified symbol with specified volume, stop-loss, and take-profit.
• `p`: Get current ask and bid prices for XAUUSD.
• `p <symbol>`: Get current ask and bid prices for specified symbol.
• `c`: Close all open positions.
• `cb`: Close all buy positions.
• `cs`: Close all sell positions.
• `o`: Get data for all open positions.
• `g <row>`: Get the chart data for XAUUSD on a 30-minute timeframe with specified rows.
• `g <row> <timeframe>`: Get the chart data for XAUUSD on specify timeframe with specified rows.
• `g <row> <timeframe> <symbol>`: Get the chart data for specified symbol and timeframe with specified rows.
• `q`: Quit the application.
## Example Usage
Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, o: opening position, g: get chart data, q: quit): a
Balance: 10000.0, Equity: 10000.0

Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, o: opening position, g: get chart data, q: quit): p EURUSD
EURUSD Ask: 1.22345, Bid: 1.22340

Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, o: opening position, g: get chart data, q: quit): b 0.1 EURUSD 0.01 0.02
Order executed successfully

Enter command (a: check balance, p: get market data, b: buy, s: sell, c: close all, o: opening position, g: get chart data, q: quit): c
Position #1234567 closed successfully
Command Details
• a: Check account balance.
• b: Buy XAUUSD with 0.1 lot.
• b <volume>: Buy XAUUSD with specified volume.
• b <volume> <symbol>: Buy specified symbol with specified volume.
• b <volume> <symbol> <sl>: Buy specified symbol with specified volume and stop-loss.
• b <volume> <symbol> <sl> <tp>: Buy specified symbol with specified volume, stop-loss, and take-profit.
• s: Sell XAUUSD with 0.1 lot.
• s <volume>: Sell XAUUSD with specified volume.
• s <volume> <symbol>: Sell specified symbol with specified volume.
• s <volume> <symbol> <sl>: Sell specified symbol with specified volume and stop-loss.
• s <volume> <symbol> <sl> <tp>: Sell specified symbol with specified volume, stop-loss, and take-profit.
• p: Get current ask and bid prices for XAUUSD.
• p <symbol>: Get current ask and bid prices for specified symbol.
• c: Close all open positions.
• cb: Close all buy positions.
• cs: Close all sell positions.
• o: Get data for all open positions.
• g <row>: Get the chart data for XAUUSD on a 30-minute timeframe with specified rows.
• g <row> <timeframe>: Get the chart data for XAUUSD on specify timeframe with specified rows.
• g <row> <timeframe> <symbol>: Get the chart data for specified symbol and timeframe with specified rows.
• q: Quit the application.