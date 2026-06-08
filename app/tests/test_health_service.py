from app.schemas.responses.health import HealthResponse
from app.services.health_service import HealthService


def test_get_health_status() -> None:
    service = HealthService()

    result = service.get_health_status()

    assert result == HealthResponse(
        status_code=200,
        detail="ok",
        result="working",
    )
