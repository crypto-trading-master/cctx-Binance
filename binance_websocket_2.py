from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import json
from pprint import pprint


def process_message(msg):
    # print("message type: {}".format(msg['e']))
    pprint(msg)
    print("Number of pairs", len(msg))
    bm.stop_socket(conn_key)
    reactor.stop()


def run():

    client = Client()

    global bm, conn_key

    bm = BinanceSocketManager(client)
    conn_key = bm.start_ticker_socket(process_message)
    # conn_key = bm.start_multiplex_socket(['!bookTicker'], process_message)
    bm.start()


if __name__ == "__main__":
    run()
