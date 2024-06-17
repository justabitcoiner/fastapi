from sqlmodel import SQLModel, Field


class JsonResponse(SQLModel):
    data: dict = Field(default={})
    message: str = Field(default="")
    status: int = Field(default=200)
