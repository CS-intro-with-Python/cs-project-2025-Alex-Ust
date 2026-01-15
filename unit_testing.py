import os
import requests


def test_wrong_route():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
    response = requests.get(f"{base_url}/non_existent_route", timeout=5)
    print("test_wrong_route \033[92mOK\033[0m" if response.status_code == 404 else "\033[91mFailed\033[0m" )
    assert response.status_code == 404

def test_home_route():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
    response = requests.get(f"{base_url}/", timeout=5)
    print("test_home_route \033[92mOK\033[0m" if response.status_code == 200 else "\033[91mFailed\033[0m" )
    assert response.status_code == 200

def test_task_with_no_title():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080/tasks/create",)
    response = requests.post(f"{base_url}", data={"details": "no title"}, allow_redirects=False)
    print("test_task_with_no_title \033[92mOK\033[0m" if response.status_code == 302 else "\033[91mFailed\033[0m" )
    assert response.status_code == 302

def test_reminder_with_no_title():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080/reminders/create",)
    response = requests.post(f"{base_url}", data={"details": "no title"}, allow_redirects=False)
    print("test_reminder_with_no_title \033[92mOK\033[0m" if response.status_code == 302 else "\033[91mFailed\033[0m" )
    assert response.status_code == 302

def test_delete_non_existent_task():
    base_url = os.environ.get("TEST_BASE_URL", "http://localhost:8080")
    response = requests.post(f"{base_url}/tasks/delete/9999", allow_redirects=False)
    print("test_delete_non_existent_task \033[92mOK\033[0m" if response.status_code == 404 else "\033[91mFailed\033[0m" )
    assert response.status_code == 404