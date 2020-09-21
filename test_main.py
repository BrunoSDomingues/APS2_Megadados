from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}