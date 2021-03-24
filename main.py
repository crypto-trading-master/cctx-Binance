import ccxt
from pprint import pprint
import time
import json


def run():
    initialize()


def initialize():

    print("\n\n---------------------------------------------------------\n\n")
    print("Welcome to Arbitr8 Bot")
    print("\n\n---------------------------------------------------------\n\n")

    try:

        global baseCoin, exchange, triplePairs, triples

        with open('config.json', 'r') as f:
            config = json.load(f)

        exchange = ccxt.binance({
            'apiKey': config['apiKey'],
            'secret': config['secret']
        })

        basePairs = []
        coinsBetween = []
        allPairs = []
        triplePairs = []

        baseCoin = config['baseCoin']

        print("Base coin:", baseCoin)

        markets = exchange.load_markets()

        # Find Trading Pairs for base coin

        print("\n\nGenerating triples...\n")

        for pair, value in markets.items():
            if isActiveMarket(value) and isSpotPair(value):
                allPairs.append(pair)
                if isBaseCoinPair(pair):
                    basePairs.append(pair)

        print("Number of valid market pairs:", len(allPairs))
        print("Number of base coin pairs:", len(basePairs))

        # Find between trading pairs

        for pair in basePairs:
            coins = pair.split("/")
            for coin in coins:
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

            # Find last Pair
            for pair2 in basePairs2:
                if pair2 != pair:
                    lastPair = pair2

                    # Find pair in between
                    baseCoinsBetween = pair.split("/")
                    quoteCoinsBetween = lastPair.split("/")
                    for baseCoinBetween in baseCoinsBetween:
                        if baseCoinBetween != baseCoin:
                            for quoteCoinBetween in quoteCoinsBetween:
                                if quoteCoinBetween != baseCoin:
                                    betweenPair = baseCoinBetween + "/" + quoteCoinBetween
                                    if betweenPair in allPairs:
                                        triple = []
                                        triple.append(pair)
                                        addTriplePair(pair)
                                        triple.append(betweenPair)
                                        addTriplePair(betweenPair)
                                        triple.append(lastPair)
                                        addTriplePair(lastPair)
                                        # Add triple to array of triples
                                        triples.append(triple)

        print("Number of Triples:", len(triples))
        print("Number of Triple Pairs:", len(triplePairs))

        calcArbitrage()

    except():
        print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")


def calcArbitrage():

    print("\n\nCalculate current market prices...")

    exchange.load_markets(True)
    tickers = exchange.fetch_tickers(triplePairs)

    for triple in triples:
        i = 0
        coinAmount = 0
        transferCoin = ''
        profit = 0

        pprint(triple)

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

                print("Profit %:", abs(1 - profit) * 100)


def isSpotPair(value):
    return value['type'] == 'spot'


def isActiveMarket(value):
    return value['info']['status'] == 'TRADING'


def isBaseCoinPair(pair):
    coins = pair.split("/")
    for coin in coins:
        if coin == baseCoin:
            return True


def addTriplePair(pair):
    if pair not in triplePairs:
        triplePairs.append(pair)


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
    run()
