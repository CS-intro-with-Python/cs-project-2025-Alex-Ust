import sys
import requests
from datetime import datetime, timedelta

BASE = "http://localhost:8080"


def main():
  def send(method, path, **kwargs):
    resp = requests.request(method, f"{BASE}{path}", timeout=5, **kwargs)
    print(f"{method} {path} -> {resp.status_code}")
    return resp

  send("GET", "/")

  item = send("POST", "/api/tasks", json={"type": "task", "title": "Test task"})
  task_id = item.json().get("id") if item.ok else None
  if task_id:
    send("PUT", f"/api/tasks/{task_id}", json={"completed": True})
    send("POST", f"/api/tasks/{task_id}/if-complete")
    send("GET", f"/api/tasks/{task_id}")

  # Reminder
  rem = send("POST", "/api/reminders", json={
    "title": "Ping",
    "scheduledTime": (datetime.now() + timedelta(minutes=30)).isoformat(),
  })
  rem_id = rem.json().get("id") if rem.ok else None
  if rem_id:
    send("PUT", f"/api/reminders/{rem_id}", json={"sent": True})
    send("DELETE", f"/api/reminders/{rem_id}")

  if task_id:
    send("DELETE", f"/api/tasks/{task_id}")


if __name__ == "__main__":
  try:
    main()
  except Exception as exc:
    print("Error:", exc)
    sys.exit(1)
