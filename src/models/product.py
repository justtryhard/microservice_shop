from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

    def get_total_price(self):
        return self.price * self.quantity


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
