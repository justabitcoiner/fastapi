from sqlmodel import SQLModel, Field


class CreateProduct(SQLModel):
    title: str
    category_id: int | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=0)
