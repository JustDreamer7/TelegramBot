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

    def run(self, func):
        crypto_price_list = {}
        lock = threading.Semaphore(12)
        symbols = ['ETHUSDT', 'EGLDUSDT', 'XRPUSDT', 'AVAXUSDT', 'SOLUSDT', 'FTTUSDT', 'WAVESUSDT', 'DOGEUSDT',
                   'ADAUSDT', 'DOCKUSDT', 'ALICEUSDT']
        # t1 = time.time()

        threads = [
            threading.Thread(target=func, args=(lock, crypto_price_list, [symbols[_]]))
            for _ in range(11)
        ]
        for th in threads:
            th.start()
            # print("Запущено потоков: %i." % threading.active_count())
        for th in threads:
            th.join()

        # t2 = time.time()
        # print(f'{11} threads time = {t2 - t1}')
        return crypto_price_list


if __name__ == "__main__":
    test = ExchangeRate(binance_api_key, binance_secret_key)
    crypto_price_list = test.run(test.historical_values)
    print(crypto_price_list)
    # print('\n')
    # print(crypto_pricechanging_list)

    #
    # def exchange_rate_my_crypto_coins(self, symbols):
    #     t1 = time.time()
    #     crypto_price_list = [float(self.client.get_symbol_ticker(symbol='ETHUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='EGLDUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='XRPUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='AVAXUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='SOLUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='FTTUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='WAVESUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='DOGEUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='ADAUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='DOCKUSDT')['price']),
    #                          float(self.client.get_symbol_ticker(symbol='ALICEUSDT')['price'])]
    #     crypto_pricechanging_list = [self.historical_values('ETHUSDT'),
    #                                  self.historical_values('EGLDUSDT'),
    #                                  self.historical_values('XRPUSDT'),
    #                                  self.historical_values('AVAXUSDT'),
    #                                  self.historical_values('SOLUSDT'),
    #                                  self.historical_values('FTTUSDT'),
    #                                  self.historical_values('WAVESUSDT'),
    #                                  self.historical_values('DOGEUSDT'),
    #                                  self.historical_values('ADAUSDT'),
    #                                  self.historical_values('DOCKUSDT'),
    #                                  self.historical_values('ALICEUSDT')]
    #     t2= time.time()
    #     print(f'func(exchange_rate_my_crypto_coins) time - {t2-t1}')
    #     return crypto_price_list, crypto_pricechanging_list
    # def historical_values(self, symbol):
    #     t1 = time.time()
    #     klines_half_day = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_12HOUR, "1 day ago UTC")
    #     klines_hour = self.client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "2 hour ago UTC")
    #     pricechanging_half_day = float(klines_half_day[1][4]) - float(klines_half_day[0][4])
    #     pricechanging_hour = float(klines_hour[1][4]) - float(klines_hour[0][4])
    #     t2 = time.time()
    #     print(f'func(exchange_rate_my_crypto_coins) time - {t2 - t1}')
    #     return [pricechanging_half_day, pricechanging_hour]
