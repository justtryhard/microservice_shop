from fastapi import APIRouter, HTTPException
from src.models.order import OrderCreate, Order
from src.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=201)
async def create_order(order_data: OrderCreate):
    try:
        order = await OrderService.create_order(order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # любые другие ошибки (включая траблы с payment srevice)
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{order_id}", response_model=Order, status_code=200)
async def get_order(order_id: int):
    try:
        return await OrderService.get_order(order_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")
