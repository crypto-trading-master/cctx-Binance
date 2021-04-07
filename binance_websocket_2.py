from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import json, pprint


def run():

    with open('secret.json', 'r') as f:
        secretFile = json.load(f)

    apiKey = secretFile['apiKey']
    secret = secretFile['secret']

    client = Client(apiKey, secret)
    btc_price = {'error':False}

    bsm = BinanceSocketManager(client)
    conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', handleTicker)
    bsm.start()


def handleTicker(msg):
    pprint(msg)



if __name__ == "__main__":
    run()
