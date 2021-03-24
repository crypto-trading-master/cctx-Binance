import ccxt
from pprint import pprint
import time
import json


def test():
    marketPrices = {}
    global exchange
    exchange = ccxt.binance()
    markets = exchange.load_markets(True)

    triples = []
    triple = ['BTC/USDT','ETH/BTC','ETH/USDT']
    triples.append(triple)

    tickers = exchange.fetch_tickers(triple)

    startBaseQty = 1

    for triple in triples:
        i = 0
        basePrice = 0
        firstPairQty = 0;
        secondPairQty = 0;
        thirdPairQty = 0;

        for pair in triple:
            i += 1

            ticker = tickers[pair]
            price = ticker['last']
            print(pair,":",price)
            if i == 1:
                firstPairQty = startBaseQty / price
                print("Quantity 1:",firstPairQty)
            if i == 2:
                secondPairQty = firstPairQty / price
                print("Quantity 2:",secondPairQty)
            if i == 3:
                thirdPairQty = secondPairQty * price
                print("Quantity 3:",thirdPairQty)
                print("Profit %:",abs(1 - (thirdPairQty / startBaseQty)) * 100)



    return



if __name__ == "__main__":
    test()
