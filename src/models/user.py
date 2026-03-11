from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    def get_info(self):
        return "Пользователь: " + self.name + ", Email: " + self.email
