from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import json
from pprint import pprint


def process_message(msg):
    # print("message type: {}".format(msg['e']))
    pprint(msg)


def run():


    client = Client()

    bm = BinanceSocketManager(client)
    # bm.start_trade_socket('BTCUSDT', process_message)
    bm.start_ticker_socket(process_message)
    bm.start()


if __name__ == "__main__":
    run()
