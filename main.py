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

        global baseCoin, exchange, triplePairs, marketPrices

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
        marketPrices = {}

        baseCoin = config['baseCoin']

        markets = exchange.load_markets()

        # Find Trading Pairs for base coin

        print("Generating triples...\n")

        ####### Write valid pairs to file for reuse ? ###########

        ####### How to get valid market info from market dict ?? ########

        for pair, value in markets.items():
            if isActiveMarket(value) and isSpotPair(value):
                allPairs.append(pair)
                if isBaseCoinPair(pair):
                    basePairs.append(pair)

        print("Number of valid market pairs: ",len(allPairs))
        print("Number of base coin pairs: ",len(basePairs))

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

        print("Number of Triples: ", len(triples))
        print("Number of Triple Pairs: ",len(triplePairs))

        #calcArbitrage()

    except():
         print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")


def calcArbitrage():

    print("Calculate current market prices...")

    for pair in triplePairs:
        depth = exchange.fetch_order_book(pair)
        bid = depth['bids'][0][0]
        ask = depth['asks'][0][0]
        marketPrices[pair] = {}
        marketPrices[pair]['bid'] = bid
        marketPrices[pair]['ask'] = ask


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

if __name__ == "__main__":
    run()
