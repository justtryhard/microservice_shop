import pytest
from pydantic import ValidationError

from src.models.product import Product, ProductCreate


def test_get_total_price_multiplies_price_and_quantity():
    product = Product(name="bread", price=2.5, quantity=4)

    assert product.get_total_price() == 10.0


@pytest.mark.parametrize(
    "price,quantity",
    [
        (0.99, 1),
        (3.0, 0),
        (5.5, 10),
    ],
)
def test_get_total_price_various_inputs(price, quantity):
    product = Product(price=price, quantity=quantity)

    assert product.get_total_price() == price * quantity


def test_get_total_price_raises_when_price_missing():
    product = Product(quantity=1)

    with pytest.raises(TypeError):
        product.get_total_price()


def test_get_total_price_raises_when_quantity_missing():
    product = Product(price=1.0)

    with pytest.raises(TypeError):
        product.get_total_price()


def test_product_create_accepts_valid_data():
    created = ProductCreate(name="cheese", price=4.5, quantity=2)

    assert created.name == "cheese"
    assert created.price == 4.5
    assert created.quantity == 2


def test_product_create_rejects_short_name():
    with pytest.raises(ValidationError):
        ProductCreate(name="a", price=1.0, quantity=1)


def test_product_create_rejects_non_positive_price():
    with pytest.raises(ValidationError):
        ProductCreate(name="rice", price=0, quantity=1)


def test_product_create_rejects_negative_quantity():
    with pytest.raises(ValidationError):
        ProductCreate(name="rice", price=1.0, quantity=-1)
