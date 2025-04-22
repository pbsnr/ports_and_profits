import random


def initialise_spices(port):
    quantity = random.randint(300, 600)
    production_rate = random.randint(1, 100)
    consumption_rate =  max(0, production_rate + random.randint(-5, 5))
    quantity_100_days = quantity + 100 * (production_rate - consumption_rate)
    price = 1000 * 1.002**(-0.05*quantity_100_days)


    spices = {
        'quantity': quantity,
        'production_rate': production_rate,
        'consumption_rate': consumption_rate,
        'price': price
    }
    return spices

def update_spices(port):

    spices = port['spices']

    if random.random() < 0.1:
        spices['production_rate'] += random.randint(-1, 1)

    if random.random() < 0.1:
        spices['consumption_rate'] += random.randint(-1, 1)
        

    production_rate = spices['production_rate']
    consumption_rate = spices['consumption_rate']
    quantity = max(spices['quantity'] + production_rate - consumption_rate, 0)
    quantity_100_days = quantity + 100 * (production_rate - consumption_rate)
    price = 1000 * 1.002**(-0.05*quantity_100_days)


    spices = {
        'quantity': quantity,
        'production_rate': production_rate,
        'consumption_rate': consumption_rate,
        'price': price
    }
    return spices


def update_spices_prices_and_quantities(ports):
    for port in ports:

        if 'spices' not in port:
            port['spices'] = initialise_spices(port)
        else:
            port['spices'] = update_spices(port)
        
    return ports