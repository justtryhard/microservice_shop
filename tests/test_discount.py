import pytest
from src.utils.calculations import calculate_discount

@pytest.fixture
def norm_price():
    return 50

@pytest.fixture
def zero_price():
    return 0

@pytest.fixture
def neg_price():
    return -50


@pytest.mark.parametrize("price, discount_rate, expected", [
                             (50, 0.1, 5),
                             (200, 0.5, 100),
                             (70, 1, 70),
                             (140, 0, 0),
                         ])

def test_calculate_discount(price, discount_rate, expected):
    assert calculate_discount(price, discount_rate) == expected

def test_norm_price(norm_price):
    assert calculate_discount(norm_price, 0.5) == 25

def test_zero_price(zero_price):
    assert calculate_discount(zero_price, 0.7) == 0

def test_neg_price(neg_price):
    assert calculate_discount(neg_price, 0.1) == -5



