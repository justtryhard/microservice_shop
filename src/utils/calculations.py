MILEAGE_RATE = 3
FREE_MILEAGE = 20


def calculate_discount(price, discount_rate):
    return price * discount_rate

def calculate_delivery(weight, mileage=20, base_cost=100) -> float:
    cost = base_cost + weight * 10
    if mileage > FREE_MILEAGE:
        cost += (mileage - FREE_MILEAGE) * MILEAGE_RATE
    return cost

def calculate_final_price(price, discount, delivery):
    return price - discount + delivery