import ccxt
from pprint import pprint
import time
import json


def test():
    marketPrices = {}
    global exchange, baseCoin
    exchange = ccxt.binance()
    markets = exchange.load_markets(True)

    baseCoin = 'BTC'

    triples = []
    triple = ['BTC/USDT','ETH/USDT','ETH/BTC']
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
                if coinIsPairBaseCoin(baseCoin, pair):
                    # Sell
                    firstFactor = ticker['ask'] * 1
                else:
                    # Buy
                    firstFactor = 1 / ticker['bid']
                print("Factor 1:",firstFactor)
            if i == 2:
                secondTransferCoin = getSecondTransferCoin(firstTransferCoin, pair)
                if coinIsPairBaseCoin(firstTransferCoin, pair):
                    secondFactor = firstFactor / ticker['bid']
                else:
                    secondFactor = firstFactor * ticker['ask']
                print("Factor 2:",secondFactor)
            if i == 3:
                if coinIsPairBaseCoin(secondTransferCoin, pair):
                    thirdFactor = secondFactor * ticker['ask']
                else:
                    thirdFactor = secondFactor / ticker['bid']

                print("Factor 3:",thirdFactor)

                print("Profit %:",abs(1 - thirdFactor) * 100)



    return

def getPairCoins(pair):
    coins = pair.split("/")
    return coins

def coinIsPairBaseCoin(coinToCheck,pair):
    coins = getPairCoins(pair)
    return coinToCheck == coins[0]

def getFirstTransferCoin(pair):
    coins = getPairCoins(pair)
    for coin in coins:
        if coin != baseCoin:
            return coin

def getSecondTransferCoin(firstTransferCoin,pair):
    coins = getPairCoins(pair)
    for coin in coins:
        if coin != firstTransferCoin:
            return coin

if __name__ == "__main__":
    test()
