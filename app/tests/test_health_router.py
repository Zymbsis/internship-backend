from fastapi.testclient import TestClient
from httpx2 import Response
from starlette.status import HTTP_200_OK

from app.schemas.responses.health import HealthResponse


def test_health_check(client: TestClient) -> None:
    response: Response = client.get("/api/")

    assert response.status_code == HTTP_200_OK

    data = HealthResponse.model_validate(response.json())
    assert data == HealthResponse(
        status_code=200,
        detail="ok",
        result="working",
    )
