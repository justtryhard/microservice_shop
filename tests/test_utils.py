import pytest
from src.utils.calculations import calculate_discount, calculate_delivery, calculate_final_price, get_usd_rate
from unittest.mock import patch


@pytest.fixture
def norm_price():
    return 50




@pytest.mark.parametrize("price, discount_rate, expected", [
    (50, 0.1, 5),
    (200, 0.5, 100),
    (70, 1, 70)
])
def test_calculate_discount(price, discount_rate, expected):
    assert calculate_discount(price, discount_rate) == expected


def test_discount_with_norm_price(norm_price):
    assert calculate_discount(norm_price, 0.5) == 25


@pytest.mark.parametrize("price, discount",
                         [
                             (100, -0.1),
                             (100, 1.5),
                             (-100, 0.1),
                         ])

def test_invalid_discount(price, discount):
    with pytest.raises(ValueError):
        calculate_discount(price, discount)



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
    "weight, mileage, base_cost",
    [
        (-1, 10, 100),
        (1, -10, 100),
        (1, 10, -100),
    ]
)
def test_invalid_delivery(weight, mileage, base_cost):
    with pytest.raises(ValueError):
        calculate_delivery(weight, mileage, base_cost)



@pytest.mark.parametrize(
    "price, discount, delivery, expected",
    [
        (1000, 100, 200, 1100),
        (500, 50, 100, 550),
        (150, 20, 100, 230)
    ]
)
def test_calculate_final_price(price, discount, delivery, expected):
    assert calculate_final_price(price, discount, delivery) == expected


@pytest.mark.parametrize(
    "price, discount, delivery, expected",
    [
        (-50, 100, 200, 1100),
        (500, -100, 100, 550),
        (150, 250, 100, 230)
    ]
)

def test_invalid_final_price(price, discount, delivery, expected):
    with pytest.raises(ValueError):
        calculate_final_price(price, discount, delivery)


@patch("src.utils.calculations.requests.get")
def test_get_usd_rate(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 85.0}}
    mock_get.return_value.status_code = 200
    result = get_usd_rate()
    assert result == 85.0
    mock_get.assert_called_once()
