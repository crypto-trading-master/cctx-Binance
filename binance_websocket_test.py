import websocket, json, pprint


def on_message(ws, message):
    pprint(message)


def on_close(ws):
    print("Websocket closed !")


if __name__ == "__main__":

    pair = 'btcusdt'

    # socketURL = f'wss://stream.binance.com:9443/ws/{pair}@kline_1m'

    socketURL = 'wss://stream.binance.com:9443/ws/!ticker@arr'

    print(socketURL)

    ws = websocket.WebSocketApp(socketURL, on_message=on_message, on_close=on_close)

    ws.run_forever()
