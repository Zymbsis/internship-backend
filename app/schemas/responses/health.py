from pydantic import BaseModel
from starlette.status import HTTP_200_OK


class HealthResponse(BaseModel):
    status_code: int = HTTP_200_OK
    detail: str = "ok"
    result: str = "working"
