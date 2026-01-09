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

  # Item with Telegram id
  item = send("POST", "/api/items", json={"type": "task", "title": "Test task", "telegramChatId": "123"})
  item_id = item.json().get("id") if item.ok else None
  if item_id:
    send("PUT", f"/api/items/{item_id}", json={"completed": True})
    send("POST", f"/api/items/{item_id}/toggle-complete")
    send("GET", f"/api/items/{item_id}")

  # Reminder
  rem_item = send("POST", "/api/items", json={"type": "reminder", "title": "Ping", "telegramChatId": "123"})
  rem_item_id = rem_item.json().get("id") if rem_item.ok else None
  if rem_item_id:
    rem = send("POST", "/api/reminders", json={
      "itemId": rem_item_id,
      "telegramChatId": "123",
      "scheduledTime": (datetime.now() + timedelta(minutes=30)).isoformat(),
    })
    rem_id = rem.json().get("id") if rem.ok else None
    if rem_id:
      send("PUT", f"/api/reminders/{rem_id}", json={"sent": True})
      send("DELETE", f"/api/reminders/{rem_id}")

  if item_id:
    send("DELETE", f"/api/items/{item_id}")
  if rem_item_id:
    send("DELETE", f"/api/items/{rem_item_id}")


if __name__ == "__main__":
  try:
    main()
  except Exception as exc:
    print("Error:", exc)
    sys.exit(1)
