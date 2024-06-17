from sqlmodel import SQLModel, Field, Identity


class User(SQLModel, table=True):
    __tablename__ = "user_"

    id: int = Field(primary_key=True, sa_column_args=[Identity(always=True)])
    username: str = Field(unique=True)
    password: str
    salt: str
