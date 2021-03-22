import ccxt
from pprint import pprint
import time
import json

def run():
    initialize()


def initialize():

    with open('config.json', 'r') as f:
        config = json.load(f)

    print("\n\n---------------------------------------------------------\n\n")
    print("Hello and Welcome to the Crypto Trader Bot Python Script")
    print("\n\n---------------------------------------------------------\n\n")

    try:        
        exchange = ccxt.binance({
            'apiKey': config['apiKey'],
            'secret': config['secret']
        })

        global baseCoin 
        baseCoin = config['baseCoin']

        markets = exchange.load_markets()
        #symbols = exchange.symbols
        #currencies = exchange.currencies
        #balances = exchange.fetchBalance()
        
        #pprint(markets['ZRX/USDT'])

        # Find Trading Pairs for base coin

        print("Generating triples...\n")

        basePairs = []
        coinsBetween = []
        allPairs = []
        
        ##### How to filter out UP / DOWN pairs ???

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
                                        triple.append(betweenPair)
                                        triple.append(lastPair)
                                        # Add triple to array of triples
                                        triples.append(triple)        
        
        print("Number of Triples: ", len(triples))
        #pprint(triples)

        '''
        arb_list = ['ETH/BTC', 'LTC/ETH', 'LTC/BTC']
        
        for sym in arb_list:
            depth = exchange.fetch_order_book(sym)
            bid = depth['bids'][0][0]
            ask = depth['asks'][0][0]
            print(sym, " Bid:", bid)
            print(sym, " Ask:", ask)
        '''

    except():
         print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")

def arbitrage():
    pass

def isBaseCoinPair(pair,value):
    if value['type'] == 'spot':
        coins = pair.split("/")
        for coin in coins:
            if coin == baseCoin:
                return True

if __name__ == "__main__":
    run()
