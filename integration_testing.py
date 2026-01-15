import os
import requests

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8080")

def test_health():
    res = requests.get(f"{BASE_URL}/health", timeout=5)
    assert res.status_code == 200


def test_db_query():
    create = requests.post(f"{BASE_URL}/api/tasks", json={"title": "integration_test", "details": "db check 💋"}, timeout=5)
    assert create.status_code == 201

    items = requests.get(f"{BASE_URL}/api/tasks", timeout=10)
    assert items.status_code == 200
