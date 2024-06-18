from sqlmodel import SQLModel, Field, Identity


class ProductCategory(SQLModel, table=True):
    __tablename__ = "product_category_"

    id: int = Field(primary_key=True, sa_column_args=[Identity(always=True)])
    title: str
