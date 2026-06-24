from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    page: int = Field(1, ge=1)
    limit: int = Field(10, gt=0, le=100)


FilterParamsDep = Annotated[FilterParams, Query()]
