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

        global baseCoin, baseCoinBalance, exchange, triplePairs, triples, \
               bestArbTriple, noOfTrades, minProfit

        basePairs = []
        coinsBetween = []
        allPairs = []
        triplePairs = []

        with open('secret.json', 'r') as f:
            secretFile = json.load(f)

        apiKey = secretFile['apiKey']
        secret = secretFile['secret']

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

        noOfTrades = config['noOfTrades']
        minProfit = config['minProfit']

        print("Exchange:", exchangeName)

        baseCoin = config['baseCoin']
        print("Base coin:", baseCoin)

        baseCoinBalance = config['startBalance']
        print("Start balance:", f"{baseCoinBalance:,}")

        markets = exchange.load_markets()

        print("\n\nGenerating triples...\n")

        # Find Trading Pairs for base coin

        for pair, value in markets.items():
            if isActiveMarket(value) and isSpotPair(value):
                allPairs.append(pair)

        tickers = exchange.fetch_tickers(allPairs)

        for pair in allPairs:
            if not tickerHasPrice(tickers[pair]):
                allPairs.remove(pair)
            else:
                if isExchangeBaseCoinPair(baseCoin, pair):

                    # ######### TODO: Check market volume

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

                        if firstTransferCoin == secondPairCoin and \
                           secondTransferCoin == thirdPairCoin:
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

        arbitrage()

    except ccxt.ExchangeError as e:
        print(str(e))


def arbitrage():
    for tradeCounter in range(noOfTrades):
        getBestArbitrageTriple()


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
        arbTriple = {}

        arbTriple['triple'] = triple

        for pair in triple:
            i += 1
            ticker = tickers[pair]

            arbTriple[pair] = {}
            arbTriple[pair]['pair'] = pair

            if i == 1:
                transferCoin = baseCoin
                coinAmount = baseCoinBalance

            if coinIsPairBaseCoin(transferCoin, pair):
                arbTriple[pair]['baseCoin'] = transferCoin
                # ######### TODO arbTriple[pair]['quoteCoin']
                # Sell
                tickerPrice = getSellPrice(ticker)
                coinAmount = tickerPrice * coinAmount
                arbTriple[pair]['tradeAction'] = 'sell'
            else:
                # ######### TODO arbTriple[pair]['baseCoin']
                arbTriple[pair]['quoteCoin'] = transferCoin
                # Buy
                tickerPrice = getBuyPrice(ticker)
                coinAmount = coinAmount / tickerPrice
                arbTriple[pair]['tradeAction'] = 'buy'

            arbTriple[pair]['calcPrice'] = tickerPrice
            arbTriple[pair]['calcAmount'] = coinAmount
            transferCoin = getTransferCoin(transferCoin, pair)
            arbTriple[pair]['transferCoin'] = transferCoin

            if i == 3:
                profit = arbTriple[pair]['calcAmount'] / baseCoinBalance
                if profit > maxProfit:
                    maxProfit = profit
                    maxTriple = triple
                    bestArbTriple = arbTriple

    maxProfit = maxProfit - 1

    print("Max. Profit % ", round((maxProfit) * 100, 2), maxTriple)
    pprint(bestArbTriple)

    if maxProfit < minProfit:
        getBestArbitrageTriple()
    else:
        doPaperTrading(bestArbTriple)

    # ############## TODO: Verify triple multiple times


def doPaperTrading(arbTriple):

    return

    i = 0

    tradeAmount = baseCoinBalance

    for pair in arbTriple['triple']:
        i += 1

        side = arbTriple[pair]['tradeAction']

        # print(pair)
        # print(tradeAmount)

        pprint(arbTriple[pair])

        if side == 'buy':
            params = {}
            type = 'market'
            amount = 0;
            price = 0;
            # params['amount'] = None
            params['quoteOrderQty'] = exchange.costToPrecision(pair, tradeAmount)
            pprint(params)
            order = exchange.create_market_buy_order(pair, amount, params)
            # order = exchange.create_order(pair, type, side, amount, price, params)
        else:
            order = exchange.create_market_sell_order(pair, tradeAmount)

        tradeAmount = order['filled']

        pprint(order)


if __name__ == "__main__":
    run()
