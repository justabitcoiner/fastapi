from fastapi import FastAPI
from src.config import Configuration
from src.jwt import Jwt
from src import models
from src.db import Engine
from src.routers import user, token

Configuration.load_config()
config = Configuration.get_config()

Jwt.gen_secret_key()
Engine.load(**config["db"])
Engine.create_new_tables()


app = FastAPI()
app.include_router(user.router)
app.include_router(token.router)


@app.get("/")
def hello_world():
    return {"message": "hello, world"}
