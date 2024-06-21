import asyncio
from typing import AsyncGenerator
import strawberry
from strawberry.fastapi import GraphQLRouter
from sqlmodel import select, insert
from src.db import Engine
from src.models.product import Product
from src.models.product_category import ProductCategory


@strawberry.experimental.pydantic.type(model=Product, all_fields=True)
class ProductGQL:
    pass


@strawberry.experimental.pydantic.type(model=ProductCategory, all_fields=True)
class ProductCategoryGQL:
    pass


def get_products(page):
    with Engine.get_session() as session:
        statement = select(Product).offset((page - 1) * 20).limit(20)
        products = session.exec(statement).all()
        products = [ProductGQL.from_pydantic(product) for product in products]
        return products


def get_product(id: int):
    with Engine.get_session() as session:
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).one_or_none()
        print("product:", product)
        if not product:
            raise Exception("Product not found")
        product = ProductGQL.from_pydantic(product)
        return product


def create_product(info):
    with Engine.get_session() as session:
        statement = insert(Product).values(**info).returning(Product.id)
        product_id = session.exec(statement).scalar_one()
        session.commit()
        return product_id


def get_product_categories():
    with Engine.get_session() as session:
        statement = select(ProductCategory)
        categories = session.exec(statement).all()
        categories = [ProductCategoryGQL.from_pydantic(categ) for categ in categories]
        return categories


@strawberry.type
class Query:
    @strawberry.field
    def products(self, page: int) -> list[ProductGQL]:
        return get_products(page)

    @strawberry.field
    def product(self, id: int) -> ProductGQL:
        return get_product(id)

    @strawberry.field
    def product_categories(self) -> list[ProductCategoryGQL]:
        return get_product_categories()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, title: str) -> int:
        return create_product({"title": title})


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)


scheme = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
router = GraphQLRouter(scheme, "/graphql")
