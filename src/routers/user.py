from fastapi.routing import APIRouter
from bcrypt import gensalt, hashpw
from src.db import Engine
from src.models.user import User
from src.schemas.user import CreateUser
from src.schemas.response import JsonResponse


router = APIRouter()
router.prefix = "/users"
router.tags = ["Users"]


@router.post("/", response_model=JsonResponse)
def create(info: CreateUser):
    salt = gensalt()
    hashed_password = hashpw(info.password.encode(), salt)

    user = User()
    user.username = info.username
    user.password = hashed_password.decode()
    user.salt = salt.decode()

    with Engine.get_session() as session:
        session.add(user)
        session.commit()
        return {"message": "Create new user success", "data": {"user_id": user.id}}
