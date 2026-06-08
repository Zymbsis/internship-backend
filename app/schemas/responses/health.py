from pydantic import BaseModel


class HealthResponse(BaseModel):
    status_code: int = 200
    detail: str = "ok"
    result: str = "working"
