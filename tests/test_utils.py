import pytest
from src.utils.calculations import calculate_discount, calculate_delivery, calculate_final_price



@pytest.mark.parametrize("order_total, rate, expected_discount",
    [
        (100, 0.9, 90),
        (200, 0.8, 160),
        (0, 0.5, 0),
        (1000, 0.1, 100)
    ]
)
def test_calculate_discount(order_total, rate, expected_discount):
    assert calculate_discount(order_total, rate) == expected_discount



@pytest.mark.parametrize("weight, base_cost, mileage, expected_delivery_price",
    [
        (1, 100, 20, 110),
        (5, 100, 90, 360),
        (0, 100, 50, 190),
        (2, 50, 10, 70)
    ]
)
def test_calculate_delivery(weight, base_cost, mileage, expected_delivery_price):
    assert calculate_delivery(weight, mileage, base_cost) == expected_delivery_price



@pytest.mark.parametrize(
    "price, discount, delivery, expected",
    [
        (1000, 100, 200, 1100),
        (500, 50, 100, 550),
        (0, 0, 0, 0),
    ]
)
def test_calculate_final_price(price, discount, delivery, expected):
    assert calculate_final_price(price, discount, delivery) == expected