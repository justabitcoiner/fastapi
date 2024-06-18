from sqlmodel import SQLModel


class CreateProductCategory(SQLModel):
    title: str
