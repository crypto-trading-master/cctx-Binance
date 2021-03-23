import ccxt
from pprint import pprint
import time
import json


def test():
    marketPrices = {}
    global exchange
    exchange = ccxt.binance()
    markets = exchange.load_markets()

    pprint(markets['ETH/BTC'])

    return

    symbols = exchange.symbols
    #pair = 'AAVE/BKRW'
    pair = 'BTC/USDT'
    #for pair in symbols:
    print(pair)
    depth = exchange.fetch_order_book(pair)
    pprint(depth)

    print(hasMarketDepth(pair))


    ask = depth['asks'][0][0]
    bid = depth['bids'][0][0]

    marketPrices[pair] = {}
    marketPrices[pair]['bid'] = bid
    marketPrices[pair]['ask'] = ask
    print(pair, " Bid:", marketPrices[pair]['bid'])
    print(pair, "Ask:", marketPrices[pair]['ask'])


if __name__ == "__main__":
    test()
