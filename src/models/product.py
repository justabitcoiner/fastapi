from sqlmodel import SQLModel, Field, Identity


class Product(SQLModel, table=True):
    __tablename__ = "product_"

    id: int = Field(primary_key=True, sa_column_args=[Identity(always=True)])
    title: str
    category_id: int | None = Field(default=None, foreign_key="product_category_.id")
    price: int | None
    quantity: int | None = Field(default=0)
