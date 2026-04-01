from src.api.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.auth import create_token
from src.models.product import Product
from src.models.user import User

client = TestClient(app)

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