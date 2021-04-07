import websocket

def on_message(wsapp, message):
    print(message)

if __name__ == "__main__":

    wsapp = websocket.WebSocketApp("wss://stream.meetup.com/2/rsvps", on_message=on_message)
    wsapp.run_forever()
