import ccxt

binance = ccxt.binance()
bybit = ccxt.bybit()

def get_price(exchange, pair):
    ticker = exchange.fetch_ticker(pair)
    return ticker["last"]
