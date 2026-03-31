def calculate_discount(price, discount_rate):
    return price * discount_rate

def calculate_delivery(weight, mileage=20, base_cost=100):
    return (base_cost + weight * 10) + (mileage - 20) * 3 if mileage > 20 else base_cost + weight * 10

def calculate_final_price(price, discount, delivery):
    return price - discount + delivery