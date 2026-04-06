import pytest
from src.models.order import Order
from src.models.product import Product
from src.models.user import User


@pytest.fixture
def sample_product1():
    return Product(name="bread", price=50, quantity=2)

@pytest.fixture
def sample_product2():
    return Product(name="milk", price=85, quantity=3)

@pytest.fixture
def sample_user():
    return User(name="TestUser", email="abc@test.com")

@pytest.fixture
def sample_order(sample_user, sample_product1, sample_product2):
    return Order(user=sample_user, products=[sample_product1, sample_product2])


def test_create_product(sample_product1):
    assert sample_product1.name == "bread"
    assert sample_product1.price == 50
    assert sample_product1.quantity == 2

def test_invalid_product_price():
    with pytest.raises(ValueError):
        Product(name="bread", price=-50, quantity=1)

def test_invalid_product_name():
    with pytest.raises(ValueError):
        Product(name="", price=100, quantity=1)

def test_invalid_product_quantity():
    with pytest.raises(Exception):
        Product(name="abc", price=50, quantity=-1)

def test_create_user(sample_user):
    assert sample_user.name == "TestUser"
    assert sample_user.email == "abc@test.com"

def test_invalid_user_name():
    with pytest.raises(Exception):
        User(name="", email="test_email@tst.com")


def test_create_order(sample_user, sample_product1, sample_product2):
    order = Order(user=sample_user, products=[sample_product1, sample_product2])
    assert order.user == sample_user
    assert order.products == [sample_product1, sample_product2]
    assert order.payment_status is False



def test_order_calculate_total(sample_order):
    assert sample_order.calculate_total() == 355

def test_empty_order(sample_user):
    with pytest.raises(Exception):
        Order(user=sample_user, products=[])


