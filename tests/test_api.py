from src.api.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.auth import create_token
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


@patch("src.api.routes.products.redis_client")
def test_get_products_cache(mock_redis):
    token = create_token(user_id=1)
    headers = {"Authorization": f"Bearer {token}"}
    mock_redis.get.return_value = '{"1": {"name": "bread", "price": 2.5}}'
    response = client.get("/api/v1/products/", headers=headers)
    assert response.status_code == 200

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

def test_get_user():
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200

def test_user_not_found():
    response = client.get("/api/v1/users/345345436")
    assert response.status_code == 404