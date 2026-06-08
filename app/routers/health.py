from fastapi import APIRouter

from app.schemas.responses.health import HealthResponse
from app.services.health_service import HealthServiceDep

router = APIRouter()


@router.get("/", response_model=HealthResponse)
def health_check(health_service: HealthServiceDep) -> HealthResponse:
    return health_service.get_health_status()
