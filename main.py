import ccxt
from functions import *
from pprint import pprint
import os
import time
import json

# pylama:ignore=W:select=F405


def run():
    initialize()


def initialize():

    print("\n---------------------------------------------------------\n")
    print("Welcome to Triangular Arbitr8 Bot")
    print("\n---------------------------------------------------------\n")

    try:

        global baseCoin, exchange, triplePairs, triples

        basePairs = []
        coinsBetween = []
        allPairs = []
        triplePairs = []

        apiKey = os.environ.get('apiKey')
        secret = os.environ.get('secret')

        with open('config.json', 'r') as f:
            config = json.load(f)

        exchangeName = config['exchangeName']
        exchange_class = getattr(ccxt, exchangeName)
        exchange = exchange_class({
            'enableRateLimit': True,
            'apiKey': apiKey,
            'secret': secret
        })
        exchange.set_sandbox_mode(True)
        print("Exchange:", exchangeName)

        baseCoin = config['baseCoin']
        print("Base coin:", baseCoin)

        markets = exchange.load_markets()

        # Find Trading Pairs for base coin

        print("\n\nGenerating triples...\n")

        for pair, value in markets.items():
            if isActiveMarket(value) and isSpotPair(value):
                allPairs.append(pair)
                if isExchangeBaseCoinPair(baseCoin, pair):
                    basePairs.append(pair)

        print("Number of valid market pairs:", len(allPairs))
        pprint(allPairs)
        print("Number of base coin pairs:", len(basePairs))

        # Find between trading pairs

        for pair in basePairs:
            coins = getPairCoins(pair)
            for coin in coins:
                if coin != baseCoin:
                    if coin not in coinsBetween:
                        coinsBetween.append(coin)

        # Check if between pair exists

        pairsBetween = []
        coinsBetween2 = coinsBetween

        for baseCoinBetween in coinsBetween:
            for qouteCoinBetween in coinsBetween2:
                pair = baseCoinBetween + "/" + qouteCoinBetween
                if pair in allPairs:
                    pairsBetween.append(pair)

        # Find triples for base coin

        # ##### Sind das wirklich alle möglichen triples ???
        # ##### Sind da auch die invertierten dabei ???

        triples = []
        basePairs2 = basePairs

        for pair in basePairs:
            firstCoins = getPairCoins(pair)
            for firstCoin in firstCoins:
                if firstCoin != baseCoin:
                    firstTransferCoin = firstCoin
            for pairBetween in pairsBetween:
                betweenPairFound = False
                secondCoins = getPairCoins(pairBetween)
                for secondCoin in secondCoins:
                    if secondCoin == firstTransferCoin:
                        betweenPairFound = True
                        secondPairCoin = secondCoin
                    else:
                        secondTransferCoin = secondCoin
                if betweenPairFound:
                    for lastPair in basePairs2:
                        thirdCoins = getPairCoins(lastPair)
                        for thirdCoin in thirdCoins:
                            if thirdCoin != baseCoin:
                                thirdPairCoin = thirdCoin

                        if firstTransferCoin == secondPairCoin and secondTransferCoin == thirdPairCoin:
                            triple = []
                            triple.append(pair)
                            addTriplePair(triplePairs, pair)
                            triple.append(pairBetween)
                            addTriplePair(triplePairs, pairBetween)
                            triple.append(lastPair)
                            addTriplePair(triplePairs, lastPair)
                            # Add triple to array of triples
                            triples.append(triple)

        print("Number of Triples:", len(triples))
        print("Number of Triple Pairs:", len(triplePairs))

        getBestArbitrageTriple()
        tradeArbitrageTriple()

    except():
        print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")


def getBestArbitrageTriple():

    print("\nCalculate current arbitrage possibilities...\n")

    exchange.load_markets(True)
    tickers = exchange.fetch_tickers(triplePairs)

    global maxProfit, maxTriple
    maxProfit = 0
    maxTriple = []

    for triple in triples:
        i = 0
        coinAmount = 0
        transferCoin = ''
        profit = 0

        # pprint(triple)

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
                # print("Factor 1:", coinAmount)
                transferCoin = getTransferCoin(baseCoin, pair)
                # print("First Transfer Coin:", transferCoin)
            if i == 2:
                if coinIsPairBaseCoin(transferCoin, pair):
                    coinAmount = coinAmount * ticker['ask']
                else:
                    coinAmount = coinAmount / ticker['bid']

                # print("Factor 2:", coinAmount)
                transferCoin = getTransferCoin(transferCoin, pair)
                # print("Second Transfer Coin:", transferCoin)

            if i == 3:
                if coinIsPairBaseCoin(transferCoin, pair):
                    profit = coinAmount * ticker['ask']
                else:
                    profit = coinAmount / ticker['bid']

                # print("Profit:", profit)

                if profit > maxProfit:
                    maxProfit = profit
                    maxTriple = triple

    print("Max. Profit % ", round((maxProfit - 1) * 100, 2), maxTriple)


def tradeArbitrageTriple():
    pass


if __name__ == "__main__":
    run()
