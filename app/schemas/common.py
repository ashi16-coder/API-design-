from pydantic import BaseModel
from typing import Any


class ErrorResponse(BaseModel):
    detail: str


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[Any]
