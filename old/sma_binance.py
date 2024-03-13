import ccxt
import threading
import pandas as pd
import time
import queue


def data(symbols: list, time_frame: str, d_queue: queue.Queue):
    client = ccxt.binanceus()
    wait_time = 0
    while True:
        df: pd.DataFrame = pd.DataFrame()
        new_time = int(wait_time / 1000) + 60
        while True:
            if time.time() > new_time:
                break

        for symbol in symbols:
            datum = client.fetch_ohlcv(symbol, time_frame, limit=500)
            df = pd.DataFrame(datum, columns=["time", "open", "high", "low", "close", "volume"])
            d_queue.put(df['close'])
        wait_time = df['time'].iloc[-1]


def sma(interval: int, d_queue: queue.Queue, s_quque: queue.Queue):
    while True:
        try:
            series: pd.Series = d_queue.get()
            print(series)
            sma_close = series.rolling(interval).mean()
            d_queue.task_done()
            s_quque.put(sma_close)
        except:
            pass


def print_sma(s_queue: queue.Queue):
    while True:
        datum = s_queue.get()
        print(datum)
        s_queue.task_done()


if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    data_queue = queue.Queue()
    sma_queue = queue.Queue()
    threading.Thread(target=sma, args=(10, data_queue, sma_queue)).start()
    threading.Thread(target=print_sma, args=(sma_queue,)).start()
    threading.Thread(target=data, args=(symbols, "1m", data_queue)).start()
