from src.models.product import ProductCreate, Product
from typing import List

class ProductService:

    @classmethod
    async def create_product(cls, product_data: ProductCreate, db) -> Product:
        new_id = max(db.keys()) + 1 if db else 1
        new_product = Product(name=product_data.name, price=product_data.price, quantity=product_data.quantity)
        db[new_id] = new_product
        return new_product

    @classmethod
    async def get_product(cls, product_id: int, db) -> Product:
        if product_id not in db:
            raise ValueError("Product not found")
        return db[product_id]

    @classmethod
    async def get_products(cls, db) -> List[Product]:
        return db
