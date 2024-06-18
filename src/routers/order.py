from fastapi import routing, Request
from sqlmodel import select, insert, or_

from src.models.order import Order
from src.models.product import Product
from src.schemas.order import CreateOrderSchema
from src.schemas.response import JSONResponseContent

router = routing.APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get("/", response_model=JSONResponseContent)
def read(req: Request, page: int = 1):
    statement = select(Order).offset((page - 1) * 20).limit(20)
    orders = req.state.session.exec(statement).all()
    orders = [order.model_dump() for order in orders]
    return JSONResponseContent(data={"orders": orders})


@router.get("/{id}", response_model=JSONResponseContent)
def read_one(req: Request, id: int):
    statement = select(Order).where(Order.id == id)
    order = req.state.session.exec(statement).one_or_none()
    if not order:
        return JSONResponseContent(message="Order not found!")
    return JSONResponseContent(data={"order": order})


@router.post("/", response_model=JSONResponseContent)
def create(req: Request, info: CreateOrderSchema):
    item_map = {}
    for item in info.items:
        item_map[item.product_id] = {"price": item.price, "quantity": item.quantity}

    statement = (
        select(Product)
        .where(or_(*[(Product.id == i.product_id) for i in info.items]))
        .with_for_update(nowait=False, of=Product)
    )
    products = req.state.session.exec(statement).all()
    if not products:
        return JSONResponseContent(message="Product not found")

    for product in products:
        if product.quantity < item_map.get(product.id).get("quantity"):
            return JSONResponseContent(
                message="Remaining quantity is not enough for this order"
            )
        product.quantity -= item_map.get(product.id).get("quantity")

    statement = insert(Order).values(info.model_dump()).returning(Order.id)
    order_id = req.state.session.exec(statement).scalar_one()
    req.state.session.commit()
    return JSONResponseContent(
        data={"id": order_id},
        message="Your order has been created",
    )
