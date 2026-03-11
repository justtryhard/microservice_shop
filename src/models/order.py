from pydantic import BaseModel, Field
from typing import Optional, List
from src.models.product import Product
from src.models.user import User


class OrderCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    product_ids: List[int] = Field(..., min_length=1)


class Order(BaseModel):
    user: Optional[User] = None
    products: Optional[List[Product]] = None
    payment_status: bool = False

    def calculate_total(self):
        total = 0
        for product in self.products:
            total = total + product.get_total_price()
        return total

