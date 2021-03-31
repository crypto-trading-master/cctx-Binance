import ccxt
from functions import *
from pprint import pprint
import json


def run():
    initialize()
    arbitrage()
    # test()


def initialize():

    print("\n---------------------------------------------------------\n")
    print("Welcome to Triangular Arbitr8 Bot")
    print("\n---------------------------------------------------------\n")

    try:

        global baseCoin, coinBalance, exchange, triplePairs, triples, \
               bestArbTriple, noOfTrades, minProfit, paperTrading

        basePairs = []
        coinsBetween = []
        allPairs = []
        triplePairs = []

        with open('config.json', 'r') as f:
            config = json.load(f)

        with open('secret.json', 'r') as f:
            secretFile = json.load(f)

        if config['useTestNet'] is True:
            apiKey = secretFile['testApiKey']
            secret = secretFile['testSecret']
        else:
            apiKey = secretFile['apiKey']
            secret = secretFile['secret']

        exchangeName = config['exchangeName']
        exchange_class = getattr(ccxt, exchangeName)
        exchange = exchange_class({
            'enableRateLimit': True,
            'apiKey': apiKey,
            'secret': secret
        })

        if config['useTestNet'] is True:
            exchange.set_sandbox_mode(True)

        paperTrading = config['paperTrading']
        noOfTrades = config['noOfTrades']
        minProfit = config['minProfit']

        print("Exchange:", exchangeName)

        baseCoin = config['baseCoin']
        print("Base coin:", baseCoin)

        coinBalance = config['startBalance']
        print("Start balance:", f"{coinBalance:,}")

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

    except ccxt.ExchangeError as e:
        print(str(e))


def arbitrage():
    for tradeCounter in range(noOfTrades):
        getBestArbitrageTriple()


def getBestArbitrageTriple():

    print("\nCalculate current arbitrage possibilities...")

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
                coinAmount = coinBalance

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
                profit = arbTriple[pair]['calcAmount'] / coinBalance
                if profit > maxProfit:
                    maxProfit = profit
                    maxTriple = triple
                    bestArbTriple = arbTriple

    maxProfit = maxProfit - 1

    print("Max. Profit % ", round((maxProfit) * 100, 2), maxTriple)

    if maxProfit < minProfit:
        getBestArbitrageTriple()
    else:
        tradeArbTriple(bestArbTriple)

    # ############## TODO: Verify triple multiple times


def tradeArbTriple(arbTriple):
    global coinBalance
    tradeAmount = coinBalance

    exchange.fetch_tickers()

    print("\nStart balance:", tradeAmount)

    for pair in arbTriple['triple']:
        side = arbTriple[pair]['tradeAction']

        print("Trading pair:", pair)
        print("Trade action:", side)
        print("Coin amount to trade:", tradeAmount)

        if paperTrading is True:
            exchange.load_markets(True)
            orderbook = (exchange.fetchOrderBook(pair))
            bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else 0
            ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else 0

            if side == 'buy':
                tradeAmount = tradeAmount / ask
            else:
                tradeAmount = tradeAmount * bid
        else:   # No Paper Trading
            if side == 'buy':
                params = {}
                amount = 0
                params['quoteOrderQty'] = exchange.costToPrecision(pair, tradeAmount)
                order = exchange.create_market_buy_order(pair, amount, params)
                # order = exchange.create_order(pair, type, side, amount, price, params)
            else:
                order = exchange.create_market_sell_order(pair, tradeAmount)

            tradeAmount = order['filled']

    print("End balance:", tradeAmount)
    coinBalance = tradeAmount

def test():

    pair = 'LTC/BNB'

    exchange.load_markets(True)
    tickers = exchange.fetch_tickers(pair)



    pprint(tickers[pair])




    pprint(exchange.fetchOrderBook(pair))



    # order = exchange.create_market_sell_order('BNB/BTC', 0.03)




if __name__ == "__main__":
    run()
