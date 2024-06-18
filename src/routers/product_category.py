from fastapi import routing, Request
from sqlmodel import select, insert
from src.models.product_category import ProductCategory
from src.schemas.product_category import CreateProductCategory
from src.schemas.response import JSONResponseContent

router = routing.APIRouter(
    prefix="/product_categories",
    tags=["Product Categories"],
)


@router.get("/", response_model=JSONResponseContent)
def read(req: Request):
    statement = select(ProductCategory)
    categories = req.state.session.exec(statement).all()
    return JSONResponseContent(data={"categories": categories})


@router.get("/{id}", response_model=JSONResponseContent)
def read_one(req: Request, id: int):
    statement = select(ProductCategory).where(ProductCategory.id == id)
    category = req.state.session.exec(statement).one_or_none()
    if not category:
        return JSONResponseContent(message="Product category not found!")
    return JSONResponseContent(data={"category": category})


@router.post("/", response_model=JSONResponseContent)
def create(req: Request, category: CreateProductCategory):
    statement = (
        insert(ProductCategory)
        .values(title=category.title)
        .returning(ProductCategory.id)
    )
    category_id = req.state.session.exec(statement).scalar_one()
    req.state.session.commit()
    return JSONResponseContent(data={"id": category_id})
