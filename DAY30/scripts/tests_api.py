import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task", "priority": 2})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task"

def test_get_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_task_insights(client):
    response = client.get("/insights/")
    assert response.status_code == 200
    data = response.json()
    assert "completed_tasks" in data
    assert "pending_tasks" in data
    assert "average_completion_time" in data
