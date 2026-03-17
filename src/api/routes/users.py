from fastapi import APIRouter, Depends, HTTPException
from src.api.auth import create_token
from src.models.user import User, UserCreate
from src.services.user_service import UserService
from src.db.db_connect import get_users_from_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=201)
async def create_user(user_data: UserCreate, db = Depends(get_users_from_db)):
    try:
        user = await UserService.create_user(user_data, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{user_id}", response_model=User, status_code=200)
async def get_user(user_id: int, db = Depends(get_users_from_db)):
    try:
        return await UserService.get_user(user_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/login")
async def login():
    # пока без БД (тест)
    return {"access_token": create_token("user1")}