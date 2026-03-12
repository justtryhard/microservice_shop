import asyncio
from typing import Dict
from unittest.mock import AsyncMock

import pytest

from src.data import orders, products, users
from src.models.order import OrderCreate
from src.services.order_service import (
    OrderService,
    PaymentProcessingError,
)


class FakePaymentClient:
    def __init__(self):
        self.process_payment = AsyncMock()


@pytest.fixture(autouse=True)
def restore_orders_state():
    snapshot: Dict[int, object] = dict(orders)
    counter_before = OrderService._order_counter
    yield
    orders.clear()
    orders.update(snapshot)
    OrderService._order_counter = counter_before


@pytest.fixture
def fake_payment_client(monkeypatch):
    client = FakePaymentClient()
    monkeypatch.setattr(OrderService, "payment_client", client)
    return client


def test_create_order_success(fake_payment_client):
    fake_payment_client.process_payment.return_value = {"status": "ok"}
    payload = OrderCreate(user_id=1, product_ids=[1, 2])

    created_order = asyncio.run(OrderService.create_order(payload))
    assert created_order.payment_status is True
    assert created_order.user == users[1]
    assert created_order.products == [products[1], products[2]]

    stored_order = orders[OrderService._order_counter]
    assert stored_order is created_order
    fake_payment_client.process_payment.assert_awaited_once()


def test_create_order_missing_user(fake_payment_client):
    fake_payment_client.process_payment.return_value = {"status": "ok"}
    payload = OrderCreate(user_id=999, product_ids=[1])

    with pytest.raises(ValueError, match="User not found"):
        asyncio.run(OrderService.create_order(payload))
    fake_payment_client.process_payment.assert_not_awaited()


def test_create_order_missing_product(fake_payment_client):
    fake_payment_client.process_payment.return_value = {"status": "ok"}
    payload = OrderCreate(user_id=1, product_ids=[999])

    with pytest.raises(ValueError, match="Product\\(s\\) not found"):
        asyncio.run(OrderService.create_order(payload))
    fake_payment_client.process_payment.assert_not_awaited()


def test_create_order_payment_failure(fake_payment_client):
    fake_payment_client.process_payment.side_effect = RuntimeError("boom")
    payload = OrderCreate(user_id=1, product_ids=[1])

    with pytest.raises(PaymentProcessingError, match="Payment processing failed for order"):
        asyncio.run(OrderService.create_order(payload))


def test_create_order_missing_status(fake_payment_client):
    fake_payment_client.process_payment.return_value = {}
    payload = OrderCreate(user_id=1, product_ids=[1])

    with pytest.raises(PaymentProcessingError, match="Payment response missing status"):
        asyncio.run(OrderService.create_order(payload))


def test_get_order_not_found():
    with pytest.raises(ValueError, match="Order not found"):
        asyncio.run(OrderService.get_order(9999))

