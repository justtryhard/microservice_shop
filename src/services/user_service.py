from src.models.user import User, UserCreate


class UserService:

    @classmethod
    async def create_user(cls, user_data: UserCreate, db) -> User:
        new_id = max(db.keys()) + 1 if db else 1
        new_user = User(name=user_data.name, email=user_data.email)
        db[new_id] = new_user
        return new_user

    @classmethod
    async def get_user(cls, user_id: int, db) -> User:
        if user_id not in db:
            raise ValueError("User not found")
        return db[user_id]

