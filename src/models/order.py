from sqlmodel import SQLModel, Field, Identity, Column, JSON


class Order(SQLModel, table=True):
    __tablename__ = "order_"

    id: int = Field(primary_key=True, sa_column_args=[Identity(always=True)])
    user_id: int = Field(foreign_key="user_.id")
    items: list[dict] = Field(sa_column=Column(JSON))
