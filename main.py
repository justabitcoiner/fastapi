from fastapi import FastAPI
from src import models
from src.db import Engine


Engine.load("psycopg2", "postgres", "postgres", "127.0.0.1", 5432, "fastapi")
Engine.create_new_tables()


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "hello, world"}
