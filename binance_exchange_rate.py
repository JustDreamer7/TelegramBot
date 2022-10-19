from config.local_settings import binance_api_key, binance_secret_key
import threading
# import requests
# import time
from binance import Client


class ExchangeRate:
    binance_api_key = binance_api_key
    binance_secret_key = binance_secret_key

    def __init__(self, binance_api_key, binance_secret_key):
        self.client = Client(binance_api_key, binance_secret_key)

    def exchange_rate_btc(self):
        klines_half_day = self.client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_12HOUR, "1 day ago UTC")
        klines_hour = self.client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "2 hour ago UTC")
        pricechanging_half_day = float(klines_half_day[1][4]) - float(klines_half_day[0][4])
        pricechanging_hour = float(klines_hour[1][4]) - float(klines_hour[0][4])
        btc_pricechanging_list = [pricechanging_half_day, pricechanging_hour]
        return float(self.client.get_symbol_ticker(symbol='BTCUSDT')['price']), btc_pricechanging_list

    def exchange_rate_my_crypto_coins(self, lock, crypto_price_list, symbols):
        with lock:
            for symbol in symbols:
                # print(symbol)
                crypto_price_list[symbol] = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
        return crypto_price_list

    def historical_values(self, lock, crypto_pricechanging_list, symbols):
        with lock:
            for symbol in symbols:
                klines_half_day = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR,
                                                                    "1 day ago UTC")
                klines_hour = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "2 hour ago UTC")
                pricechanging_half_day = float(klines_half_day[1][4]) - float(klines_half_day[0][4])
                pricechanging_hour = float(klines_hour[1][4]) - float(klines_hour[0][4])
                crypto_pricechanging_list[symbol] = (pricechanging_half_day, pricechanging_hour)
        return crypto_pricechanging_list

    @staticmethod
    def run(func):
        crypto_price_list = {}
        lock = threading.Semaphore(12)
        symbols = ['ETHUSDT', 'EGLDUSDT', 'XRPUSDT', 'AVAXUSDT', 'SOLUSDT', 'FTTUSDT', 'WAVESUSDT', 'DOGEUSDT',
                   'ADAUSDT', 'DOCKUSDT', 'ALICEUSDT']

        threads = [
            threading.Thread(target=func, args=(lock, crypto_price_list, [symbols[_]]))
            for _ in range(11)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        return crypto_price_list


if __name__ == "__main__":
    test = ExchangeRate(binance_api_key, binance_secret_key)
    crypto_price_list = test.run(test.historical_values)
    print(crypto_price_list)
