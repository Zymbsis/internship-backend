from typing import Annotated

from fastapi import Depends

from app.schemas.responses.health import HealthResponse


class HealthService:
    def get_health_status(self) -> HealthResponse:
        return HealthResponse()


HealthServiceDep = Annotated[HealthService, Depends()]
