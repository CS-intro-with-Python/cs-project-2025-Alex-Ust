import os
import requests


def test_wrong_route():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
    response = requests.get(f"{base_url}/non_existent_route", timeout=5)
    assert response.status_code == 404

def test_home_route():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
    response = requests.get(f"{base_url}/", timeout=5)
    assert response.status_code == 200

def test_task_with_no_title():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080/tasks/create",)
    response = requests.post(f"{base_url}", data={"details": "no title"}, allow_redirects=False)
    assert response.status_code == 302

def test_reminder_with_no_title():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080/reminders/create",)
    response = requests.post(f"{base_url}", data={"details": "no title"}, allow_redirects=False)
    assert response.status_code == 302

def test_delete_non_existent_task():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
    response = requests.post(f"{base_url}/tasks/delete/9999", allow_redirects=False)
    assert response.status_code == 404