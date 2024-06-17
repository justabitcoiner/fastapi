from sqlmodel import SQLModel


class CreateUser(SQLModel):
    username: str
    password: str
