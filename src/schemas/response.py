from sqlmodel import SQLModel, Field


class JsonResponse(SQLModel):
    status: int = Field(default=200)
    message: str = Field(default="")
    data: dict = Field(default={})
