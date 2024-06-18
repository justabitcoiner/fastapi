from sqlmodel import SQLModel


class CreateOrderSchema(SQLModel):
    user_id: int
    items: list["OrderItemSchema"]


class OrderItemSchema(SQLModel):
    product_id: int
    price: int
    quantity: int
