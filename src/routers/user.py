from fastapi import Request
from fastapi.routing import APIRouter
from bcrypt import gensalt, hashpw
from src.models.user import User
from src.schemas.user import CreateUser
from src.schemas.response import JSONResponseContent


router = APIRouter()
router.prefix = "/users"
router.tags = ["Users"]


@router.post("/", response_model=JSONResponseContent)
def create(info: CreateUser, req: Request):
    salt = gensalt()
    hashed_password = hashpw(info.password.encode(), salt)

    user = User()
    user.username = info.username
    user.password = hashed_password.decode()
    user.salt = salt.decode()
    req.state.session.add(user)
    req.state.session.commit()
    return {"message": "Create new user success", "data": {"user_id": user.id}}
