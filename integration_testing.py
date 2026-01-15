import os
import requests

BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:8080")

def test_health():
    res = requests.get(f"{BASE_URL}/health", timeout=5)
    print("test_health \033[92mOK\033[0m" if res.status_code == 200 else "\033[91mFailed\033[0m" )
    assert res.status_code == 200


def test_db_query():
    create = requests.post(f"{BASE_URL}/api/tasks", json={"title": "integration_test", "details": "db check 💋"}, timeout=5)
    print("test_db_query created task with ID:", create.json().get("id"), "\033[92mOK\033[0m" if create.status_code == 201 else "\033[91mFailed\033[0m" )
    assert create.status_code == 201

    items = requests.get(f"{BASE_URL}/api/tasks", timeout=10)
    print("test_db_query fetched tasks \033[92mOK\033[0m" if items.status_code == 200 else "\033[91mFailed\033[0m" )
    assert items.status_code == 200

    item_delete = requests.delete(f"{BASE_URL}/api/tasks/{create.json().get('id')}", timeout=5)
    print("test_db_query deleted task \033[92mOK\033[0m" if item_delete.status_code == 200 else "\033[91mFailed\033[0m" )
    assert item_delete.status_code == 200
