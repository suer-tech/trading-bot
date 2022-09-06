from binance.spot import Spot
import time
import key

client = Spot(key="key", secret="secret")

def lot():
    lot = int(11 / price)
    return lot

def balance_token():
    acc = client.account()
    list = acc['balances']
    for crypto in list:
        if crypto['asset'] == "SHIB":
            balance_token = (crypto['free'])
    return float(balance_token)

def order_limit_buy(i):
    params = {
        'symbol': 'SHIBUSDT',
        'side': 'BUY',
        'type': 'LIMIT',
        "timeInForce": "GTC",
        'quantity': lot(),
        'price': price_limit(price, i)
    }
    client.new_order(**params)

def price_limit(price_order_1, i):
    price_limit = round((float(price) - delta * i), 8)
    return f"{price_limit:.{8}f}"

def price_sell():
    price_sell = round((float(price_order_1) + delta), 8)
    return f"{price_sell:.{8}f}"

def order_sell():
    vol = client.my_trades(symbol='SHIBUSDT')[-1]['qty']
    coms = client.my_trades(symbol='SHIBUSDT')[-1]['commission']
    qty = round(float(vol) - float(coms))
    params = {
        'symbol': 'SHIBUSDT',
        'side': 'SELL',
        'type': 'LIMIT',
        "timeInForce": "GTC",
        'quantity': str(qty),
        'price': price_sell()
    }
    client.new_order(**params)

while True:
    delta = 0.00000010
    all_orders = client.get_open_orders(symbol='SHIBUSDT')
    my_trade = client.my_trades(symbol='SHIBUSDT')
    price = float(client.ticker_price(symbol='SHIBUSDT')['price'])
    price_order_1 = client.my_trades(symbol='SHIBUSDT')[-1]['price']
    i = 1

    if (balance_token() < lot()) and (len(all_orders) == 0):
        while i < 11:
            order_limit_buy(i)
            i += 1

    elif len(all_orders) > 0:
        last_order_price = all_orders[-1]['price']
        last_trade = my_trade[-1]['isBuyer']

        if (price_sell() != last_order_price) and (last_trade == True):
            order_sell()

    time.sleep(5)

