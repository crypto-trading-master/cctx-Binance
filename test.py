import ccxt
from pprint import pprint
import time
import json


def test():

    global exchange, baseCoin
    exchange = ccxt.binance()
    markets = exchange.load_markets(True)

    baseCoin = 'USDT'

    triples = []
    triple = ['BTC/USDT', 'ETH/BTC', 'ETH/USDT']
    triples.append(triple)

    tickers = exchange.fetch_tickers(triple)

    for triple in triples:
        i = 0
        coinAmount = 0
        transferCoin = ''
        profit = 0

        for pair in triple:
            i += 1
            ticker = tickers[pair]

            if i == 1:
                if coinIsPairBaseCoin(baseCoin, pair):
                    # Sell
                    coinAmount = ticker['ask'] * 1
                else:
                    # Buy
                    coinAmount = 1 / ticker['bid']
                print("Factor 1:", coinAmount)
                transferCoin = getTransferCoin(baseCoin, pair)
                print("First Transfer Coin:", transferCoin)
            if i == 2:
                if coinIsPairBaseCoin(transferCoin, pair):
                    coinAmount = coinAmount() * ticker['ask']
                else:
                    coinAmount = coinAmount / ticker['bid']

                print("Factor 2:", coinAmount)
                transferCoin = getTransferCoin(transferCoin, pair)
                print("Second Transfer Coin:", transferCoin)

            if i == 3:
                if coinIsPairBaseCoin(transferCoin, pair):
                    profit = coinAmount * ticker['ask']
                else:
                    profit = coinAmount / ticker['bid']

                print("Profit:", profit)

                print("Profit %:", abs(1 - profit) * 100)


def getPairCoins(pair):
    coins = pair.split("/")
    return coins


def coinIsPairBaseCoin(coinToCheck, pair):
    coins = getPairCoins(pair)
    return coinToCheck == coins[0]


def getTransferCoin(lastCoin, pair):
    coins = getPairCoins(pair)
    for coin in coins:
        if coin != lastCoin:
            return coin


if __name__ == "__main__":
    test()
