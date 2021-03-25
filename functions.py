def isSpotPair(value):
    return value['type'] == 'spot'


def isActiveMarket(value):
    return value['info']['status'] == 'TRADING'


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
