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
        #symbols = exchange.symbols
        #currencies = exchange.currencies
        #balances = exchange.fetchBalance()
        
        #pprint(markets['ZRX/USDT'])

        # Find Trading Pairs for base coin

        print("Generating triples...\n")        
                
        for pair, value in markets.items():
            allPairs.append(pair)

            if isBaseCoinPair(pair,value):
                basePairs.append(pair)        

        #print("Base pairs:\n")
        #pprint(basePairs)

        # Find between trading pairs

        for pair in basePairs:
            coins = pair.split("/")
            for coin in coins:
                if coin not in coinsBetween:
                    coinsBetween.append(coin)        
        
        #print("Between pair Coins:\n")
        #pprint(coinsBetween)

        # Check if between pair exists

        pairsBetween = []
        coinsBetween2 = coinsBetween

        for baseCoinBetween in coinsBetween:
            for qouteCoinBetween in coinsBetween2:
                pair = baseCoinBetween + "/" + qouteCoinBetween
                if pair in allPairs:
                    pairsBetween.append(pair)

        #print("Between pairs:\n")
        #pprint(pairsBetween)
        
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

        calcArbitrage()
        

        '''
        
        
        for sym in arb_list:
            depth = exchange.fetch_order_book(sym)
            bid = depth['bids'][0][0]
            ask = depth['asks'][0][0]
            print(sym, " Bid:", bid)
            print(sym, " Ask:", ask)
        '''

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


def isBaseCoinPair(pair,value):
    if value['type'] == 'spot':
        coins = pair.split("/")
        for coin in coins:
            if coin == baseCoin:
                return True

def addTriplePair(pair):
    pass
    '''
    if pair not in triplePairs:
        triplePairs.append(pair)
    '''

def test():
    marketPrices = {}
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    symbols = exchange.symbols
    for pair in symbols:    
        print(pair)
        depth = exchange.fetch_order_book(pair)
        bid = depth['bids'][0][0]
        ask = depth['asks'][0][0]        
        marketPrices[pair] = {}
        marketPrices[pair]['bid'] = bid
        marketPrices[pair]['ask'] = ask
        print(pair, " Bid:", marketPrices[pair]['bid'])
        print(pair, "Ask:", marketPrices[pair]['ask'])


if __name__ == "__main__":
    #run()
    test()