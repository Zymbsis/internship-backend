from collections.abc import Iterator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with (
        patch("app.db.postgres.connect", new=AsyncMock()),
        patch("app.db.redis.initialize", new=AsyncMock()),
        TestClient(app) as test_client,
    ):
        yield test_client
