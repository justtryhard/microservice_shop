from pydantic import BaseModel, field_validator, Field
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=0, max_length=100)

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name should not be empty')
        return v.strip()

class User(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    email: Optional[str] = Field(..., min_length=0, max_length=100)

    def get_info(self):
        return "Пользователь: " + self.name + ", Email: " + self.email

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name should not be empty')
        return v.strip()