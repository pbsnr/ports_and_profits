def buy(port, boat, money, hour):
    enough_spices = port['spices']['quantity'] >= boat['quantity']
    can_afford = boat['quantity'] * port['spices']['price'] <= money
    has_space = boat['cargo_used'] + boat['quantity'] <= boat['cargo_size']
    
    if enough_spices and can_afford and has_space:

        port['spices']['quantity'] -= boat['quantity']
        boat['cargo_used'] += boat['quantity']
        money -= boat['quantity'] * port['spices']['price']
        print([hour, -boat['cargo_used'] * port['spices']['price']])
        boat["accounting_history"].append([hour, (boat['cargo_used'] * port['spices']['price'])*-1])
        boat["accounting_history"] = boat["accounting_history"][-100:]

        
    else:
        print("Not enough spices or money to buy.")
    
    return port, boat, money

def sell(port, boat, money, hour):
    port['spices']['quantity'] += boat['cargo_used']
    money += boat['cargo_used'] * port['spices']['price']
    print([hour, boat['cargo_used'] * port['spices']['price']])
    boat["accounting_history"].append([hour, boat['cargo_used'] * port['spices']['price']])
    boat["accounting_history"] = boat["accounting_history"][-100:]
    boat['cargo_used'] = 0

    return port, boat, money
    

def trade(boat, port, money, hour):
    if boat['buy'] == port['name']:
        print(f"Boat {boat['name']} is buying from {port['name']}")
        port, boat, money = buy(port, boat, money, hour)
    elif boat['sell'] == port['name']:
        print(f"Boat {boat['name']} is selling to {port['name']}")
        port, boat, money = sell(port, boat, money, hour)
    else:
        print(f"Boat {boat['name']} is not trading at {port['name']}")

    return boat, port, money