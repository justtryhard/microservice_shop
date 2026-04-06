from src.api.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.auth import create_token, verify_token
from src.models.product import Product
from src.models.user import User


client = TestClient(app)

@patch("src.api.auth.SECRET_KEY", "testsecret")
@patch("src.api.auth.ALGORITHM", "HS256")
@patch("src.api.routes.products.redis_client")
@patch("src.services.product_service.ProductService.get_products")
def test_get_products(mock_get_products, mock_redis_client):
    token = create_token(user_id=1)
    headers = {"Authorization": f"Bearer {token}"}
    mock_redis_client.get.return_value = None
    mock_get_products.return_value = {1: {"name": "bread", "price": 2.5}, 2: {"name": "curd", "price": 3.0}}
    response = client.get("/api/v1/products/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "1" in data or 1 in data
    mock_get_products.assert_called_once()
    mock_redis_client.get.assert_called_once()

def test_get_products_unauthorized():
    response = client.get("/api/v1/products/")
    assert response.status_code == 401

@patch("src.api.auth.SECRET_KEY", "testsecret")
@patch("src.api.auth.ALGORITHM", "HS256")
@patch("src.api.routes.products.redis_client")
def test_get_products_cache(mock_redis):
    token = create_token(user_id=1)
    headers = {"Authorization": f"Bearer {token}"}
    mock_redis.get.return_value = '{"1": {"name": "bread", "price": 2.5}}'
    response = client.get("/api/v1/products/", headers=headers)
    assert response.status_code == 200


@patch("src.api.auth.SECRET_KEY", "testsecret")
@patch("src.api.auth.ALGORITHM", "HS256")
@patch("src.api.routes.products.redis_client")
@patch("src.services.product_service.ProductService.get_products")
def test_get_products_empty(mock_get_products, mock_redis):
    token = create_token(user_id=1)
    headers = {"Authorization": f"Bearer {token}"}
    mock_redis.get.return_value = None
    mock_get_products.return_value = {}

    response = client.get("/api/v1/products/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {}


@patch("src.data.users")
@patch("src.data.products")
@patch("src.services.order_service.PaymentClient.process_payment")
def test_create_order(mock_payment, mock_products, mock_users):
    mock_users.return_value = User(name="test", email="test@test.com")
    mock_products.return_value = {1: Product(name="bread", price=2.5, quantity=2), 2: Product(name="curd", price=3.0, quantity=1)}
    mock_payment.return_value = {"status": "ok"}
    response = client.post("/api/v1/orders/", json={
        "user_id": 1, "product_ids": [1, 2]})
    assert response.status_code == 201
    data = response.json()
    assert data["payment_status"] is True
    mock_payment.assert_called_once()

def test_create_invalid_order():
    response = client.post("/api/v1/orders/", json={
        "user_id": None,
        "product_ids": []
    })
    assert response.status_code == 422

@patch("src.data.users")
@patch("src.data.products")
def test_create_order_product_not_found(mock_products, mock_users):
    mock_users.return_value = User(name="test", email="test@test.com")
    mock_products.return_value = {}
    response = client.post("/api/v1/orders/", json={
        "user_id": 1,
        "product_ids": [252354]
    })
    assert response.status_code == 400


@patch("src.data.users")
@patch("src.data.products")
def test_create_order_one_of_products_not_found(mock_products, mock_users):
    mock_users.return_value = User(name="test", email="a@b.com")
    mock_products.return_value = {1: Product(name="bread", price=2.5, quantity=1)}
    response = client.post("/api/v1/orders/", json={
        "user_id": 1,
        "product_ids": [1, 459]
    })
    assert response.status_code == 400

def test_create_order_without_products():
    response = client.post("/api/v1/orders/", json={
        "user_id": 1,
        "product_ids": []
    })
    assert response.status_code == 422


def test_create_order_invalid_user():
    response = client.post("/api/v1/orders/", json={
        "user_id": "abc",
        "product_ids": [1, 2]
    })
    assert response.status_code == 422

def test_create_order_invalid_product():
    response = client.post("/api/v1/orders/", json={
        "user_id": 1,
        "product_ids": ["dfsdf"]
    })
    assert response.status_code == 422

def test_create_order_without_products_field():
    response = client.post("/api/v1/orders/", json={
        "user_id": 1,
    })
    assert response.status_code == 422

def test_create_order_without_user_field():
    response = client.post("/api/v1/orders/", json={
        "product_ids": [1, 2, 3]
    })
    assert response.status_code == 422

def test_create_order_without_field():
    response = client.post("/api/v1/orders/", json={})
    assert response.status_code == 422


def test_create_user():
    response = client.post("/api/v1/users", json={
        "name": "alex",
        "email": "alex@test.com"
    })
    assert response.status_code == 201

def test_create_user_invalid_name():
    response = client.post("/api/v1/users", json={
        "name": "",
        "email": "g4rf34tw4y"
    })
    assert response.status_code == 422

def test_create_user_without_name():
    response = client.post("/api/v1/users", json={
        "email": "g4rf34tw4y"
    })
    assert response.status_code == 422

def test_create_user_without_email():
    response = client.post("/api/v1/users", json={
        "name": "alex",
    })
    assert response.status_code == 422

def test_create_user_without_fields():
    response = client.post("/api/v1/users", json={})
    assert response.status_code == 422

def test_get_user():
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200

def test_get_user_invalid():
    response = client.get("/api/v1/users/asd")
    assert response.status_code == 422

def test_user_not_found():
    response = client.get("/api/v1/users/345345436")
    assert response.status_code == 404


@patch("src.api.routes.exchange.exchange_client")
def test_convert_price(mock_client):
    mock_client.get_exchange_rate.return_value = 2.0
    response = client.get("api/v1/currency/convert", params={
        "price": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 200
    assert response.json() == 200
    mock_client.get_exchange_rate.assert_called_once_with("USD", "EUR")


def test_convert_same_currency():
    response = client.get("api/v1/currency/convert", params={
        "price": 50,
        "from_currency": "USD",
        "to_currency": "USD"
    })
    assert response.status_code == 200
    assert response.json() == 50


@patch("src.api.routes.exchange.exchange_client")
def test_convert_service_unavailable(mock_client):
    mock_client.get_exchange_rate.return_value = None
    response = client.get("api/v1/currency/convert", params={
        "price": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 503
    data = response.json()
    assert data["detail"] == "service unavailable"


@patch("src.api.routes.exchange.exchange_client")
def test_convert_zero_price(mock_client):
    mock_client.get_exchange_rate.return_value = 2.0
    response = client.get("api/v1/currency/convert", params={
        "price": 0,
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 200
    assert response.json() == 0


@patch("src.api.routes.exchange.exchange_client")
def test_convert_invalid_currency(mock_client):
    mock_client.get_exchange_rate.return_value = None
    response = client.get("api/v1/currency/convert", params={
        "price": 100,
        "from_currency": "dsdsdf",
        "to_currency": "wegdre"
    })
    assert response.status_code == 503
    assert response.json()["detail"] == "service unavailable"

@patch("src.api.auth.SECRET_KEY", "testsecret")
@patch("src.api.auth.ALGORITHM", "HS256")
def test_create_token_returns_str():
    token = create_token(user_id=123)
    assert isinstance(token, str)


@patch("src.api.auth.SECRET_KEY", "testsecret")
@patch("src.api.auth.ALGORITHM", "HS256")
def test_verify_token_valid():
    token = create_token(user_id=456)
    user_id = verify_token(token)
    assert user_id == 456


