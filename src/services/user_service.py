from src.models.user import User, UserCreate
from src.data import users


class UserService:

    @classmethod
    async def create_user(cls, user_data: UserCreate) -> User:
        new_id = max(users.keys()) + 1 if users else 1
        new_user = User(name=user_data.name, email=user_data.email)
        users[new_id] = new_user
        return new_user

    @classmethod
    async def get_user(cls, user_id: int) -> User:
        if user_id not in users:
            raise ValueError("User not found")
        return users[user_id]

