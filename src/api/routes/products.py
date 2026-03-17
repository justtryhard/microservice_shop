from fastapi import APIRouter, Depends, HTTPException
from src.api.auth import get_current_user
from src.models.product import Product, ProductCreate
from src.services.product_service import ProductService
import redis, json

router = APIRouter(prefix="/products", tags=["products"])

redis_client = redis.Redis(host="localhost", port=6379, db=0, socket_timeout=0.5)

@router.post("/", response_model=Product, status_code=201)
async def create_product(product_data: ProductCreate):
    try:
        product = await ProductService.create_product(product_data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{product_id}", response_model=Product, status_code=200)
async def get_product(product_id: int):
    try:
        return await ProductService.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")

@router.get("/")
async def get_products():
    try:
        cached = redis_client.get("products")
        if cached:
            return json.loads(cached)
        products = await ProductService.get_products()
        redis_client.setex("products", 3600, json.dumps(products))
        return products
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):# если редис недоступен, идём сразу в БД
        print('Redis is not available')
        return await ProductService.get_products()