from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import json
from pprint import pprint
import threading, time

orderBook = {}
watchPair = 'ADAUSDT'


def process_ticker(msg):
    global orderBook

    for pair in msg:
        symbol = pair['s']
        orderBook[symbol] = {}
        orderBook[symbol]['ask'] = pair['a']
        orderBook[symbol]['bid'] = pair['b']


def run():

    client = Client()

    global bm, conn_key

    bm = BinanceSocketManager(client)
    conn_key = bm.start_ticker_socket(process_ticker)
    bm.start()

    i = 0
    WAIT_TIME_SECONDS = 4
    ticker = threading.Event()

    while not ticker.wait(WAIT_TIME_SECONDS):
        i += 1
        print("Ask:", orderBook[watchPair]['ask'])
        print("Bid:", orderBook[watchPair]['bid'])
        if i == 5:
            break

    bm.stop_socket(conn_key)
    reactor.stop()

if __name__ == "__main__":
    run()
