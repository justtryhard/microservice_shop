from src.models.product import ProductCreate, Product
from src.data import products
from typing import List


class ProductService:

    @classmethod
    async def create_product(cls, product_data: ProductCreate) -> Product:
        new_id = max(products.keys()) + 1 if products else 1
        new_product = Product(name=product_data.name, price=product_data.price, quantity=product_data.quantity)
        products[new_id] = new_product
        return new_product

    @classmethod
    async def get_product(cls, product_id: int) -> Product:
        if product_id not in products:
            raise ValueError("Product not found")
        return products[product_id]

    @classmethod
    async def get_products(cls) -> List[Product]:
        return products
