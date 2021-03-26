import ccxt
from functions import *
from pprint import pprint
import os
import time
import json


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
        if config['testMode'] is True:
            exchange.set_sandbox_mode(True)

        print("Exchange:", exchangeName)

        baseCoin = config['baseCoin']
        print("Base coin:", baseCoin)

        markets = exchange.load_markets()

        print("\n\nGenerating triples...\n")

        # Find Trading Pairs for base coin

        for pair, value in markets.items():
            if isActiveMarket(value) and isSpotPair(value):
                allPairs.append(pair)
                if isExchangeBaseCoinPair(baseCoin, pair):

                    # ######### TO DO: Check market volume

                    basePairs.append(pair)

        print("Number of valid market pairs:", len(allPairs))
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

    except ccxt.ExchangeError as e:
        print(str(e))


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

        for pair in triple:
            i += 1
            ticker = tickers[pair]

            if i == 1:
                if coinIsPairBaseCoin(baseCoin, pair):
                    # Sell
                    coinAmount = getSellPrice(ticker) * 1
                else:
                    # Buy
                    coinAmount = 1 / getBuyPrice(ticker)
                transferCoin = getTransferCoin(baseCoin, pair)
            if i == 2:
                if coinIsPairBaseCoin(transferCoin, pair):
                    coinAmount = coinAmount * getSellPrice(ticker)
                else:
                    coinAmount = coinAmount / getBuyPrice(ticker)
                transferCoin = getTransferCoin(transferCoin, pair)

            if i == 3:
                if coinIsPairBaseCoin(transferCoin, pair):
                    profit = coinAmount * getSellPrice(ticker)
                else:
                    profit = coinAmount / getBuyPrice(ticker)

                if profit > maxProfit:
                    maxProfit = profit
                    maxTriple = triple

    print("Max. Profit % ", round((maxProfit - 1) * 100, 2), maxTriple)

    # ############## TO DO: Verify triple multiple times

    doPaperTrading()


def doPaperTrading():
    pass


if __name__ == "__main__":
    run()
