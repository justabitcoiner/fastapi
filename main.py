from fastapi import FastAPI
from src.config import Configuration
from src import models
from src.db import Engine
from src.routers import user

Configuration.load_config()
config = Configuration.get_config()
Engine.load(**config["db"])
Engine.create_new_tables()


app = FastAPI()
app.include_router(user.router)


@app.get("/")
def hello_world():
    return {"message": "hello, world"}
