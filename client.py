import sys
import requests
from datetime import datetime, timedelta

BASE = "http://localhost:8080"


def main():
  def send(method, path, **kwargs):
    resp = requests.request(method, f"{BASE}{path}", timeout=5, **kwargs)
    print(f"METHOD:\033[36m{method}\033[0m PATH:\033[34m{path}\033[0m -> \033[35m{resp.status_code}\033[0m")
    return resp

  send("GET", "/")

#================= Task API tests ==================#
  print("\n--- Task API Tests ---\n")
  item = send("POST", "/api/tasks", json={"type": "task", "title": "test task"})
  task_id = item.json().get("id") if item.ok else None
  if task_id:
    send("PUT", f"/api/tasks/{task_id}", json={"completed": True})
    send("POST", f"/api/tasks/{task_id}/if-complete")
    send("GET", f"/api/tasks/{task_id}")
    send("DELETE", f"/api/tasks/{task_id}")

#================= Reminder API tests ==================#
  print("\n--- Reminder API Tests ---\n")
  rem = send("POST", "/api/reminders", json={"title": "reminder", "details": "test reminder", "scheduledTime": (datetime.now() + timedelta(minutes=30)).isoformat()})
  rem_id = rem.json().get("id") if rem.ok else None
  if rem_id:
    send("PUT", f"/api/reminders/{rem_id}", json={"sent": True})
    send("POST", f"/api/reminders/{rem_id}/if-complete")
    send("GET", f"/api/reminders/{rem_id}")
    send("DELETE", f"/api/reminders/{rem_id}")




if __name__ == "__main__":
  try:
    main()
  except Exception as exc:
    print("Error:", exc)
    sys.exit(1)
