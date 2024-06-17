from fastapi.routing import APIRouter
from sqlmodel import select
from bcrypt import hashpw
from src.db import Engine
from src.models.user import User
from src.schemas.user import CreateUser
from src.schemas.response import JsonResponse
from src.jwt import Jwt


router = APIRouter()
router.prefix = "/tokens"
router.tags = ["Tokens"]


@router.post("/new", response_model=JsonResponse)
def get_new_token(info: CreateUser):
    with Engine.get_session() as session:
        statement = select(User).where(User.username == info.username)
        user = session.exec(statement).one_or_none()
        if not user:
            raise Exception("User doesn't exist")

        hashed_password = hashpw(info.password.encode(), user.salt.encode())
        if hashed_password.decode() != user.password:
            raise Exception("Password is incorrect")

        access_token = Jwt.gen_token(user.id)
        return {
            "message": "Get access token success",
            "data": {"access_token": access_token},
        }
