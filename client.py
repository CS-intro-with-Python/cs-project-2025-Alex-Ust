

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8080"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_test(name, status, details=""):
    """Print test result with color coding."""
    status_symbol = "✓" if status else "✗"
    color = GREEN if status else RED
    print(f"{color}{status_symbol}{RESET} {name}")
    if details:
        print(f"  {details}")


def test_endpoint(method, url, expected_status=200, data=None, params=None):
    """Test an endpoint and return True if reachable and returns expected status."""
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        else:
            return False, f"Unknown method: {method}"
        
        is_success = response.status_code == expected_status
        details = f"Status: {response.status_code} (expected {expected_status})"
        return is_success, details
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - is the server running?"
    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    print(f"\n{BLUE}{'='*60}")
    print("Testing API Endpoints Reachability")
    print(f"{'='*60}{RESET}\n")
    
    # Track test results
    test_results = []
    
    # Track created IDs for cleanup and dependent tests
    created_ids = {
        "user_id": None,
        "item_id": None,
        "reminder_id": None,
    }
    
    # ==================== ROOT ENDPOINT ====================
    print(f"{YELLOW}Root Endpoint{RESET}")
    print("-" * 60)
    status, details = test_endpoint("GET", f"{BASE_URL}/")
    print_test("GET /", status, details)
    test_results.append(("GET /", status))
    print()
    
    # ==================== USER ENDPOINTS ====================
    print(f"{YELLOW}User Endpoints{RESET}")
    print("-" * 60)
    
    # GET /api/users (empty)
    status, details = test_endpoint("GET", f"{BASE_URL}/api/users")
    print_test("GET /api/users", status, details)
    test_results.append(("GET /api/users", status))
    
    # GET /api/users with email filter
    status, details = test_endpoint("GET", f"{BASE_URL}/api/users", params={"email": "test@example.com"})
    print_test("GET /api/users?email=test@example.com", status, details)
    test_results.append(("GET /api/users?email=test@example.com", status))
    
    # POST /api/users (create)
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "telegramChatId": "123456789",
        "timezone": "UTC"
    }
    status, details = test_endpoint("POST", f"{BASE_URL}/api/users", expected_status=201, data=user_data)
    print_test("POST /api/users", status, details)
    test_results.append(("POST /api/users", status))
    
    # Get created user ID
    if status:
        try:
            response = requests.get(f"{BASE_URL}/api/users", params={"email": "test@example.com"})
            if response.status_code == 200:
                users = response.json()
                if users:
                    created_ids["user_id"] = users[0]["id"]
        except:
            pass
    
    # GET /api/users/<user_id>
    if created_ids["user_id"]:
        status, details = test_endpoint("GET", f"{BASE_URL}/api/users/{created_ids['user_id']}")
        print_test(f"GET /api/users/{created_ids['user_id']}", status, details)
        test_results.append((f"GET /api/users/{created_ids['user_id']}", status))
    else:
        test_id = "test-user-id"
        status, details = test_endpoint("GET", f"{BASE_URL}/api/users/{test_id}", expected_status=404)
        print_test(f"GET /api/users/{test_id} (not found)", status, details)
        test_results.append((f"GET /api/users/{test_id} (not found)", status))
    
    # PUT /api/users/<user_id>
    if created_ids["user_id"]:
        update_data = {"name": "Updated User", "timezone": "America/New_York"}
        status, details = test_endpoint("PUT", f"{BASE_URL}/api/users/{created_ids['user_id']}", data=update_data)
        print_test(f"PUT /api/users/{created_ids['user_id']}", status, details)
        test_results.append((f"PUT /api/users/{created_ids['user_id']}", status))
    
    # DELETE /api/users/<user_id>
    if created_ids["user_id"]:
        status, details = test_endpoint("DELETE", f"{BASE_URL}/api/users/{created_ids['user_id']}")
        print_test(f"DELETE /api/users/{created_ids['user_id']}", status, details)
        test_results.append((f"DELETE /api/users/{created_ids['user_id']}", status))
    print()
    
    # ==================== ITEM ENDPOINTS ====================
    print(f"{YELLOW}Item Endpoints{RESET}")
    print("-" * 60)
    
    # GET /api/items (empty)
    status, details = test_endpoint("GET", f"{BASE_URL}/api/items")
    print_test("GET /api/items", status, details)
    test_results.append(("GET /api/items", status))
    
    # GET /api/items with filters
    status, details = test_endpoint("GET", f"{BASE_URL}/api/items", params={"type": "task", "completed": "false"})
    print_test("GET /api/items?type=task&completed=false", status, details)
    test_results.append(("GET /api/items?type=task&completed=false", status))
    
    # POST /api/items (create)
    item_data = {
        "type": "task",
        "title": "Test Task",
        "details": "This is a test task",
        "tags": ["test", "demo"],
        "datetime": (datetime.now() + timedelta(days=1)).isoformat(),
        "completed": False
    }
    status, details = test_endpoint("POST", f"{BASE_URL}/api/items", expected_status=201, data=item_data)
    print_test("POST /api/items", status, details)
    test_results.append(("POST /api/items", status))
    
    # Get created item ID
    if status:
        try:
            response = requests.get(f"{BASE_URL}/api/items")
            if response.status_code == 200:
                items = response.json()
                if items:
                    created_ids["item_id"] = items[0]["id"]
        except:
            pass
    
    # GET /api/items/<item_id>
    if created_ids["item_id"]:
        status, details = test_endpoint("GET", f"{BASE_URL}/api/items/{created_ids['item_id']}")
        print_test(f"GET /api/items/{created_ids['item_id']}", status, details)
        test_results.append((f"GET /api/items/{created_ids['item_id']}", status))
    else:
        test_id = "test-item-id"
        status, details = test_endpoint("GET", f"{BASE_URL}/api/items/{test_id}", expected_status=404)
        print_test(f"GET /api/items/{test_id} (not found)", status, details)
        test_results.append((f"GET /api/items/{test_id} (not found)", status))
    
    # PUT /api/items/<item_id>
    if created_ids["item_id"]:
        update_data = {"title": "Updated Task", "completed": True}
        status, details = test_endpoint("PUT", f"{BASE_URL}/api/items/{created_ids['item_id']}", data=update_data)
        print_test(f"PUT /api/items/{created_ids['item_id']}", status, details)
        test_results.append((f"PUT /api/items/{created_ids['item_id']}", status))
    
    # POST /api/items/<item_id>/toggle-complete
    if created_ids["item_id"]:
        status, details = test_endpoint("POST", f"{BASE_URL}/api/items/{created_ids['item_id']}/toggle-complete")
        print_test(f"POST /api/items/{created_ids['item_id']}/toggle-complete", status, details)
        test_results.append((f"POST /api/items/{created_ids['item_id']}/toggle-complete", status))
    
    # DELETE /api/items/<item_id>
    if created_ids["item_id"]:
        status, details = test_endpoint("DELETE", f"{BASE_URL}/api/items/{created_ids['item_id']}")
        print_test(f"DELETE /api/items/{created_ids['item_id']}", status, details)
        test_results.append((f"DELETE /api/items/{created_ids['item_id']}", status))
    print()
    
    # ==================== TAG ENDPOINTS ====================
    print(f"{YELLOW}Tag Endpoints{RESET}")
    print("-" * 60)
    
    # GET /api/tags
    status, details = test_endpoint("GET", f"{BASE_URL}/api/tags")
    print_test("GET /api/tags", status, details)
    test_results.append(("GET /api/tags", status))
    
    # GET /api/tags/<tag_name>
    test_tag = "work"
    status, details = test_endpoint("GET", f"{BASE_URL}/api/tags/{test_tag}", expected_status=404)
    print_test(f"GET /api/tags/{test_tag} (not found)", status, details)
    test_results.append((f"GET /api/tags/{test_tag} (not found)", status))
    
    # GET /api/tags/<tag_name>/items
    status, details = test_endpoint("GET", f"{BASE_URL}/api/tags/{test_tag}/items")
    print_test(f"GET /api/tags/{test_tag}/items", status, details)
    test_results.append((f"GET /api/tags/{test_tag}/items", status))
    print()
    
    # ==================== REMINDER ENDPOINTS ====================
    print(f"{YELLOW}Reminder Endpoints{RESET}")
    print("-" * 60)
    
    # GET /api/reminders
    status, details = test_endpoint("GET", f"{BASE_URL}/api/reminders")
    print_test("GET /api/reminders", status, details)
    test_results.append(("GET /api/reminders", status))
    
    # GET /api/reminders with filters
    status, details = test_endpoint("GET", f"{BASE_URL}/api/reminders", params={"sent": "false"})
    print_test("GET /api/reminders?sent=false", status, details)
    test_results.append(("GET /api/reminders?sent=false", status))
    
    # Create a test item first for reminder
    test_item_data = {
        "type": "reminder",
        "title": "Test Reminder Item",
        "details": "For reminder testing"
    }
    test_item_id = None
    try:
        response = requests.post(f"{BASE_URL}/api/items", json=test_item_data)
        if response.status_code == 201:
            test_item_id = response.json().get("id")
    except:
        pass
    
    # POST /api/reminders (create)
    if test_item_id:
        reminder_data = {
            "itemId": test_item_id,
            "telegramChatId": "123456789",
            "scheduledTime": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        status, details = test_endpoint("POST", f"{BASE_URL}/api/reminders", expected_status=201, data=reminder_data)
        print_test("POST /api/reminders", status, details)
        test_results.append(("POST /api/reminders", status))
        
        # Get created reminder ID
        if status:
            try:
                response = requests.get(f"{BASE_URL}/api/reminders")
                if response.status_code == 200:
                    reminders = response.json()
                    if reminders:
                        created_ids["reminder_id"] = reminders[0]["id"]
            except:
                pass
    else:
        print_test("POST /api/reminders", False, "Skipped - no test item available")
        test_results.append(("POST /api/reminders", False))
    
    # GET /api/reminders/<reminder_id>
    if created_ids["reminder_id"]:
        status, details = test_endpoint("GET", f"{BASE_URL}/api/reminders/{created_ids['reminder_id']}")
        print_test(f"GET /api/reminders/{created_ids['reminder_id']}", status, details)
        test_results.append((f"GET /api/reminders/{created_ids['reminder_id']}", status))
    else:
        test_id = "test-reminder-id"
        status, details = test_endpoint("GET", f"{BASE_URL}/api/reminders/{test_id}", expected_status=404)
        print_test(f"GET /api/reminders/{test_id} (not found)", status, details)
        test_results.append((f"GET /api/reminders/{test_id} (not found)", status))
    
    # PUT /api/reminders/<reminder_id>
    if created_ids["reminder_id"]:
        update_data = {"sent": True}
        status, details = test_endpoint("PUT", f"{BASE_URL}/api/reminders/{created_ids['reminder_id']}", data=update_data)
        print_test(f"PUT /api/reminders/{created_ids['reminder_id']}", status, details)
        test_results.append((f"PUT /api/reminders/{created_ids['reminder_id']}", status))
    
    # DELETE /api/reminders/<reminder_id>
    if created_ids["reminder_id"]:
        status, details = test_endpoint("DELETE", f"{BASE_URL}/api/reminders/{created_ids['reminder_id']}")
        print_test(f"DELETE /api/reminders/{created_ids['reminder_id']}", status, details)
        test_results.append((f"DELETE /api/reminders/{created_ids['reminder_id']}", status))
    
    # Cleanup test item
    if test_item_id:
        try:
            requests.delete(f"{BASE_URL}/api/items/{test_item_id}")
        except:
            pass
    
    print()
    print(f"{BLUE}{'='*60}")
    
    # Summary
    total_tests = len(test_results)
    passed_tests = sum(1 for _, status in test_results if status)
    failed_tests = total_tests - passed_tests
    
    print(f"Testing Complete")
    print(f"Total: {total_tests} | Passed: {GREEN}{passed_tests}{RESET} | Failed: {RED}{failed_tests}{RESET}")
    print(f"{'='*60}{RESET}\n")
    
    # Exit with error code if any tests failed
    if failed_tests > 0:
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
