import ccxt
from pprint import pprint
import time
import json

def run():
    initialize()
    

def initialize():

    with open('config.json', 'r') as f:
        config = json.load(f)

    #Create List of Crypto Pairs to Watch
    list_of_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT','BNBBTC', 'ETHBTC', 'LTCBTC']
    micro_cap_coins = ['ICXBNB', 'BRDBNB', 'NAVBNB', 'RCNBNB']
    #time_horizon = "Short"
    #Risk = "High"
    print("\n\n---------------------------------------------------------\n\n")
    print("Hello and Welcome to the Crypto Trader Bot Python Script")
    print("\n\n---------------------------------------------------------\n\n")
    
    #time.sleep(5)

    try:
        #Get Status of Exchange & Account
        #print("Number of Exchanges: ", len(ccxt.exchanges))
        #print("List of available exchanges: \n\n")
        #print(ccxt.exchanges)

        binance = ccxt.binance({
            'apiKey': config['apiKey'],
            'secret': config['secret']
        })

        coins = ['BTC']

        markets = binance.load_markets()
        symbols = binance.symbols
        currencies = binance.currencies
        balances = binance.fetchBalance()

        #print("Exchange: ", binance.id)
        #print("Exchange limits: ", binance.rateLimit)
        #print("Number of Markets: ", len(markets))
        #print("Number of Symbols: ", len(symbols))
        #print("Number of Currencies: ", len(currencies))
        #pprint(balances)            

        # Find Trading Pairs for base currencies

        pairs = []

        for symbol in symbols:
            for coin in coins:
                if coin in symbol:
                    pairs.append(symbol)
        
        #print(pairs)

        # From coin 1 to coin 2 Bid
        # From coin 2 to coin 3 Ask        
        # From coin 3 to coin 1 Bid

        arb_list = ['ETH/BTC', 'LTC/ETH', 'LTC/BTC']

        for sym in arb_list:
            depth = binance.fetch_order_book(symbol = sym)
            pprint(depth)
        

    except():
         print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")        
    
def arbitrage():
    pass

if __name__ == "__main__":
    run()