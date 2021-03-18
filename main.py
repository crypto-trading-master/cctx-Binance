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
        print("Number of Exchanges: ", len(ccxt.exchanges))
        #print("List of available exchanges: \n\n")
        #print(ccxt.exchanges)

        binance = ccxt.binance({
            'apiKey': config['apiKey'],
            'secret': config['secret']
        })

        markets = binance.load_markets()
        symbols = binance.symbols
        currencies = binance.currencies
        balances = binance.fetchBalance()

        print("Exchange: ", binance.id)
        print("Exchange limits: ", binance.rateLimit)
        print("Number of Markets: ", len(markets))
        print("Number of Symbols: ", len(symbols))
        print("Number of Currencies: ", len(currencies))
        #pprint(balances)            

    except():
         print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")        
    
if __name__ == "__main__":
    run()