from src.database.user_db import create_user, get_user_by_id



user = create_user("test", "test@mail1.com")
print(user)

print(get_user_by_id(user["id"]))