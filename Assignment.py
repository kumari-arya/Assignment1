import csv

# Function to calculate the profit and loss (PNL) for a paired trade
def calculate_pnl(open_trade, close_trade):
    pnl = (float(close_trade['PRICE']) - float(open_trade['PRICE'])) * min(int(open_trade['QUANTITY']), int(close_trade['QUANTITY']))
    return pnl

# Read trades from the input file
trades = []
with open('trades.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        trades.append(row)

# Initialize variables
opening_trades = {}
closing_trades = {}

# Iterate through trades
for trade in trades:
    symbol = trade['SYMBOL']
    side = trade['SIDE']
    quantity = int(trade['QUANTITY'])

    if side == 'B':
        # Opening trade
        if symbol not in opening_trades:
            opening_trades[symbol] = []
        opening_trades[symbol].append(trade)

    elif side == 'S':
        # Closing trade
        if symbol in opening_trades and opening_trades[symbol]:
            opening_trade = opening_trades[symbol][0]
            pnl = calculate_pnl(opening_trade, trade)
            closing_trades.setdefault(symbol, [])
            closing_trades[symbol].append({
                'open_trade': opening_trade,
                'close_trade': trade,
                'quantity': min(int(opening_trade['QUANTITY']), quantity),
                'pnl': pnl
            })
            opening_trade_quantity = int(opening_trade['QUANTITY'])
            if quantity < opening_trade_quantity:
                opening_trade['QUANTITY'] = str(opening_trade_quantity - quantity)
            else:
                opening_trades[symbol].pop(0)
                if len(opening_trades[symbol]) == 0:
                    del opening_trades[symbol]

# Print paired trades in chronological order
print("OPEN_TIME, CLOSE_TIME, SYMBOL, QUANTITY, PNL, OPEN_SIDE, CLOSE_SIDE, OPEN_PRICE, CLOSE_PRICE")
for symbol in closing_trades:
    trades = closing_trades[symbol]
    for trade in trades:
        print(f"{int(trade['open_trade']['TIME'])}, {int(trade['close_trade']['TIME'])}, {symbol}, {trade['quantity']}, "
              f"{float(trade['pnl']):.2f}, {trade['open_trade']['SIDE']}, {trade['close_trade']['SIDE']}, "
              f"{float(trade['open_trade']['PRICE']):.2f}, {float(trade['close_trade']['PRICE']):.2f}")

# Calculate cumulative realized PNL
cumulative_pnl = sum(float(trade['pnl']) for symbol in closing_trades for trade in closing_trades[symbol])
print(f"\n{float(cumulative_pnl):.2f}")