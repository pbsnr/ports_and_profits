def log_day_accounting(boat, trade_money):
    boat["accounting_history"].append(trade_money)

    return boat

def update_boat_accounting(boat, hour):

    day = hour // 24

    print(f"Boat {boat['name']} accounting: {boat['accounting_history']}")

    boat['accounting_formatted'].append([day, boat['accounting_formatted'][-1][1] + sum(boat["accounting_history"])])
    boat['accounting_formatted'] = boat['accounting_formatted'][-50:]
    boat["accounting_history"] = []
    return boat



def buy(port, boat, money, hour):
    enough_spices = port['spices']['quantity'] >= boat['quantity']
    can_afford = boat['quantity'] * port['spices']['price'] <= money
    has_space = boat['cargo_used'] + boat['quantity'] <= boat['cargo_size']
    
    if enough_spices and can_afford and has_space:

        port['spices']['quantity'] -= boat['quantity']
        boat['cargo_used'] += boat['quantity']
        money -= boat['quantity'] * port['spices']['price']
        log_day_accounting(boat, -boat['cargo_used'] * port['spices']['price'])

        
    else:
        print("Not enough spices or money to buy.")
    
    return port, boat, money

def sell(port, boat, money, hour):
    port['spices']['quantity'] += boat['cargo_used']
    money += boat['cargo_used'] * port['spices']['price']
    log_day_accounting(boat, boat['cargo_used'] * port['spices']['price'])
    boat['cargo_used'] -= boat['quantity']

    return port, boat, money
    

def trade(boat, port, money, hour):
    if boat['buy'] == port['name']:
        port, boat, money = buy(port, boat, money, hour)
    elif boat['sell'] == port['name']:
        port, boat, money = sell(port, boat, money, hour)

    return boat, port, money