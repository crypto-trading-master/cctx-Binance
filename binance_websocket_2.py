from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import json
from pprint import pprint

i = 0
j = 0

def process_symbol_ticker(msg):
    global i
    i += 1

    print("ask Ticker:", msg['a'])
    print("bid Ticker:", msg['b'])

    if i == 5:
        bm1.stop_socket(conn_key1)
        # reactor.stop()


def process_book_ticker(msg):
    global j
    j += 1

    print("ask Book:", msg['a'])
    print("bid Book:", msg['b'])

    if j == 50:
        bm2.stop_socket(conn_key2)
        # reactor.stop()

def run():

    client = Client()

    global bm1, bm2, conn_key1, conn_key2

    bm1 = BinanceSocketManager(client)
    bm2 = BinanceSocketManager(client)
    conn_key1 = bm1.start_symbol_ticker_socket('ADAUSDT', process_symbol_ticker)
    conn_key2 = bm2.start_symbol_book_ticker_socket('ADAUSDT', process_book_ticker)
    # conn_key = bm.start_ticker_socket(process_message)
    # conn_key = bm.start_multiplex_socket(['!bookTicker'], process_message)
    bm1.start()
    # bm2.start()


if __name__ == "__main__":
    run()
