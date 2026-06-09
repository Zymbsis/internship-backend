from starlette.status import HTTP_200_OK

from app.schemas.responses.health import HealthResponse
from app.services.health_service import HealthService


def test_get_health_status() -> None:
    service = HealthService()

    result = service.get_health_status()

    assert result == HealthResponse(
        status_code=HTTP_200_OK,
        detail="ok",
        result="working",
    )
