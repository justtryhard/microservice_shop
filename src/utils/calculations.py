import requests

MILEAGE_RATE = 3
FREE_MILEAGE = 20


def calculate_discount(price, discount_rate):
    if not 0 < discount_rate <= 1 or price < 0:
        raise ValueError
    return price * discount_rate

def calculate_delivery(weight, mileage=20, base_cost=100) -> float:
    if weight < 0 or mileage <= 0 or base_cost <= 0:
        raise ValueError
    cost = base_cost + weight * 10
    if mileage > FREE_MILEAGE:
        cost += (mileage - FREE_MILEAGE) * MILEAGE_RATE
    return cost

def calculate_final_price(price, discount, delivery):
    if price <= discount or delivery < 0 or price < 0 or discount <= 0:
        raise ValueError
    return price - discount + delivery

def get_usd_rate():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    return data["rates"]["RUB"]