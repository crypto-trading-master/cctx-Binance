import ccxt
from pprint import pprint
import time
import json


def test():
    marketPrices = {}
    global exchange
    exchange = ccxt.binance()
    markets = exchange.load_markets(True)

    baseCoin = 'USDT'

    triples = []
    triple = ['BTC/USDT','ETH/BTC','ETH/USDT']
    triples.append(triple)

    tickers = exchange.fetch_tickers(triple)

    startBaseQty = 1

    for triple in triples:
        i = 0
        basePrice = 0
        firstFactor = 0;
        firstTransferCoin = ''
        secondFactor = 0;
        secondTransferCoin = ''
        thirdFactor = 0;

        for pair in triple:
            i += 1
            ticker = tickers[pair]

            if i == 1:
                firstTransferCoin = getFirstTransferCoin(pair)
                if coinIsBaseCoin(baseCoin, pair):
                    # Sell
                    firstFactor = ticker['ask'] / 1                    
                else:
                    # Buy
                    firstFactor := 1 / ticker['bid']
                print("Factor 1:",firstFactor)
            if i == 2:
                secondPairQty = firstPairQty / price
                print("Quantity 2:",secondPairQty)
            if i == 3:
                thirdPairQty = secondPairQty * price
                print("Quantity 3:",thirdPairQty)
                print("Profit %:",abs(1 - (thirdPairQty / startBaseQty)) * 100)



    return

def coinIsBaseCoin(coinToCheck,pair):
    coins = pair.split("/")
    return coinToCheck == coins[0]

def getFirstTransferCoin(pair):
    coins = pair.split("/")
    for coin in coins:
        if coin != baseCoin
            return coin

if __name__ == "__main__":
    test()
