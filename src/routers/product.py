from fastapi import Request
from fastapi.routing import APIRouter
from sqlmodel import select, insert, update, delete
from src.models.product import Product
from src.schemas.product import CreateProduct, UpdateProduct
from src.schemas.response import JSONResponseContent

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=JSONResponseContent)
def read(req: Request, page: int = 1):
    statement = select(Product).offset((page - 1) * 20).limit(20)
    products = req.state.session.exec(statement).all()
    products = [product.model_dump() for product in products]
    return JSONResponseContent(data={"products": products})


@router.get("/{id}", response_model=JSONResponseContent)
def read_one(req: Request, id: int):
    statement = select(Product).where(Product.id == id)
    product = req.state.session.exec(statement).one_or_none()
    if not product:
        return JSONResponseContent(message="Product not found!")
    return JSONResponseContent(data={"product": product})


@router.post("/", response_model=JSONResponseContent)
def create(req: Request, info: CreateProduct):
    statement = insert(Product).values(info.model_dump()).returning(Product.id)
    product_id = req.state.session.exec(statement).scalar_one()
    req.state.session.commit()
    return JSONResponseContent(data={"id": product_id})


@router.put("/{id}", response_model=JSONResponseContent)
def update_product(req: Request, id: int, info: UpdateProduct):
    statement = (
        update(Product)
        .where(Product.id == id)
        .values(info.model_dump(exclude_none=True))
        .returning(Product.id)
    )
    product_id = req.state.session.exec(statement).one_or_none()
    req.state.session.commit()
    if not product_id:
        return JSONResponseContent(message="Product not found!")
    return JSONResponseContent(message="Update product successfully.")


@router.delete("/{id}", response_model=JSONResponseContent)
def delete_product(req: Request, id: int):
    statement = delete(Product).where(Product.id == id)
    req.state.session.exec(statement)
    req.state.session.commit()
    return JSONResponseContent(message="Delete product successfully.")
