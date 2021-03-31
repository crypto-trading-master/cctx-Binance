def isSpotPair(value):
    return value['type'] == 'spot'


def isActiveMarket(value):
    return value['active'] is True


def isExchangeBaseCoinPair(baseCoin, pair):
    coins = getPairCoins(pair)
    for coin in coins:
        if coin == baseCoin:
            return True


def addTriplePair(triplePairs, pair):
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


def tickerHasPrice(ticker):
    return ticker['ask'] != 0 and ticker['bid'] != 0


def getBuyPrice(ticker):
    return ticker['ask']  # ask


def getSellPrice(ticker):
    return ticker['bid']  # bid
