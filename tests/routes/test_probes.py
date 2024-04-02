from fastapi.testclient import TestClient
from requests import Response

from src.app import app

client = TestClient(app)


class TestProbesRoutes:
    def test_alive_endpoint(self):
        response: Response = client.get("/api/v1/alive")
        assert response.status_code == 200
        assert response.json() == {"alive": True}
