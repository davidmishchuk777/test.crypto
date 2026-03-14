import ccxt
import time
import threading
from signals import add_signal

# Биржи
exchanges = {
    "binance": ccxt.binance(),
    "bybit": ccxt.bybit(),
    "mexc": ccxt.mexc(),
    "gate": ccxt.gateio(),
    "okx": ccxt.okx(),
    "kucoin": ccxt.kucoin()
}

# Минимальный спред в %
MIN_SPREAD = 0.5

# Найти все USDT пары на каждой бирже
def get_usdt_pairs(exchange):
    try:
        markets = exchange.load_markets()
        pairs = [symbol for symbol in markets if symbol.endswith("/USDT")]
        return pairs
    except Exception as e:
        print(f"Error loading pairs from {exchange.id}: {e}")
        return []

# Сканирование спредов между биржами
def scan():
    # Подготовка всех USDT пар
    all_pairs = {}
    for name, ex in exchanges.items():
        pairs = get_usdt_pairs(ex)
        all_pairs[name] = pairs
        print(f"{name}: {len(pairs)} USDT pairs loaded")

    while True:
        try:
            # Сравниваем все пары между биржами
            for pair in set(pair for pairs in all_pairs.values() for pair in pairs):
                prices = {}
                # Получаем цену каждой биржи, если есть пара
                for name, ex in exchanges.items():
                    if pair in all_pairs[name]:
                        try:
                            ticker = ex.fetch_ticker(pair)
                            prices[name] = ticker['last']
                        except Exception as e:
                            print(f"Error fetching {pair} on {name}: {e}")

                # Ищем максимальный и минимальный
                if len(prices) < 2:
                    continue

                max_ex = max(prices, key=lambda k: prices[k])
                min_ex = min(prices, key=lambda k: prices[k])
                max_price = prices[max_ex]
                min_price = prices[min_ex]
                spread = (max_price - min_price) / min_price * 100

                if spread >= MIN_SPREAD:
                    signal = {
                        "pair": pair,
                        "buy": min_ex,
                        "buy_price": min_price,
                        "sell": max_ex,
                        "sell_price": max_price,
                        "spread": round(spread, 2)
                    }
                    add_signal(signal)
                    print("SIGNAL:", signal)

        except Exception as e:
            print("Scan error:", e)

        time.sleep(5)  # пауза между сканами

# Запуск в отдельном потоке
def start_scanner():
    thread = threading.Thread(target=scan)
    thread.daemon = True
    thread.start()
