import pytest

from src.models.order import Order
from src.models.product import Product
from src.models.user import User



def test_create_order():
    """Тест: создание заказа"""
    product1 = Product(name="bread", price=50, quantity=2)
    product2 = Product(name="cheese", price=150, quantity=3)
    product3 = Product(name="milk", price=85, quantity=1)
    products = [product1, product2, product3]
    user1 = User(name="TestUser", email="test@test.com")
    order = Order(user=user1, products=products)
    assert order.user == user1
    assert order.products == products
    assert order.payment_status is False



def test_calculate_total():
    """Тест: расчет стоимости заказа"""
    product1 = Product(name="bread", price=50, quantity=2)
    product2 = Product(name="cheese", price=150, quantity=3)
    product3 = Product(name="milk", price=85, quantity=1)
    products = [product1, product2, product3]
    user1 = User(name="TestUser", email="test@test.com")
    order = Order(user=user1, products=products)
    total = order.calculate_total()
    assert total == 635
