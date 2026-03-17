from fastapi import APIRouter, HTTPException, Depends
from src.models.order import OrderCreate, Order
from src.db.db_connect import get_products_from_db, get_orders_from_db, get_users_from_db
from src.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=201)
async def create_order(
        order_data: OrderCreate,
        users_db = Depends(get_users_from_db),
        products_db = Depends(get_products_from_db),
        orders_db = Depends(get_orders_from_db)
        ):
    try:
        order = await OrderService.create_order(order_data, users_db, products_db, orders_db)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # любые другие ошибки (включая траблы с payment srevice)
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{order_id}", response_model=Order, status_code=200)
async def get_order(order_id: int, orders_db = Depends(get_orders_from_db)):
    try:
        return await OrderService.get_order(order_id, orders_db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")
