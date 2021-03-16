import ccxt
import time
#import save_historical_data_Roibal

#from Keys import Key1

def run():
    # get system status
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
        print("\nExchange Status: \n\n")
        print(ccxt.exchanges)

    except():
         print("\n \n \nATTENTION: NON-VALID CCTX CONNECTION \n \n \n")        
    
    
if __name__ == "__main__":
    run()