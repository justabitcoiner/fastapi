from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.config import Configuration
from src.jwt import Jwt
from src import models
from src.db import Engine
from src.routers import user, token
from src.schemas.response import JSONResponseContent

config = Configuration.get_config()
Jwt.gen_secret_key()
Engine.load(**config["db"])
Engine.create_new_tables()


app = FastAPI()
app.include_router(user.router)
app.include_router(token.router)


@app.middleware("http")
async def use_session(req: Request, call_next):
    with Engine.get_session() as session:
        req.state.session = session
        return await call_next(req)


@app.exception_handler(Exception)
def handle_exception(request: Request, exc: Exception):
    return JSONResponse(JSONResponseContent(message=str(exc)).model_dump())
