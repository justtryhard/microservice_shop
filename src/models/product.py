from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('name should not be empty')
        return v.strip()

class Product(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

    def get_total_price(self):
        return self.price * self.quantity

