from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid
from models import Item, ItemType, Tag, Reminder, User

app = Flask(__name__)

# In-memory storage (will be replaced with database later)
items_store = {}
tags_store = {}
reminders_store = {}
users_store = {}


@app.route("/")
def hello():
    return render_template("index.html")


# ==================== USER ENDPOINTS ====================


@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Get all users, optionally filtered by email address.
    Query parameters:
        - email: Filter by user email (case-insensitive exact match)
    """
    users = list(users_store.values())

    email = request.args.get("email")
    if email:
        email = email.lower()
        users = [user for user in users if user.email and user.email.lower() == email]

    return jsonify([user.to_dict() for user in users])


@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user by ID."""
    if user_id not in users_store:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users_store[user_id].to_dict())


@app.route("/api/users", methods=["POST"])
def create_user():
    """Create a new user."""
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    user_id = data.get("id") or str(uuid.uuid4())

    if user_id in users_store:
        return jsonify({"error": "User with this ID already exists"}), 409

    user = User(
        id=user_id,
        name=data["name"],
        email=data.get("email"),
        telegram_chat_id=data.get("telegramChatId"),
        timezone=data.get("timezone"),
    )

    users_store[user_id] = user
    return jsonify(user.to_dict()), 201


@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update an existing user."""
    if user_id not in users_store:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user = users_store[user_id]

    if "name" in data:
        user.name = data["name"].strip()
    if "email" in data:
        user.email = data["email"].lower().strip() if data["email"] else None
    if "telegramChatId" in data:
        user.telegram_chat_id = data["telegramChatId"]
    if "timezone" in data:
        user.timezone = data["timezone"]

    user.updated_at = datetime.now()

    return jsonify(user.to_dict())


@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user."""
    if user_id not in users_store:
        return jsonify({"error": "User not found"}), 404

    del users_store[user_id]
    return jsonify({"message": "User deleted"}), 200


# ==================== ITEM ENDPOINTS ====================

@app.route("/api/items", methods=["GET"])
def get_items():
    """
    Get all items, optionally filtered by type, tag, or search query.
    Query parameters:
        - type: Filter by item type (note, reminder, task)
        - tag: Filter by tag name
        - search: Search in title and details
        - completed: Filter by completion status (true/false)
    """
    items = list(items_store.values())
    
    # Apply filters
    item_type = request.args.get("type")
    if item_type:
        items = [item for item in items if item.type.value == item_type]
    
    tag_filter = request.args.get("tag")
    if tag_filter:
        items = [item for item in items if tag_filter.lower() in [t.lower() for t in item.tags]]
    
    search = request.args.get("search", "").lower()
    if search:
        items = [item for item in items 
                if search in item.title.lower() or search in item.details.lower()]
    
    completed = request.args.get("completed")
    if completed is not None:
        completed_bool = completed.lower() == "true"
        items = [item for item in items if item.completed == completed_bool]
    
    return jsonify([item.to_dict() for item in items])


@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id):
    """Get a specific item by ID."""
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(items_store[item_id].to_dict())


@app.route("/api/items", methods=["POST"])
def create_item():
    """Create a new item."""
    data = request.get_json()
    
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    item_id = data.get("id") or str(uuid.uuid4())
    item_type = ItemType(data.get("type", "note"))
    
    # Parse datetime if provided
    datetime_value = None
    if data.get("datetime"):
        try:
            datetime_value = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            pass
    
    item = Item(
        id=item_id,
        type=item_type,
        title=data["title"],
        details=data.get("details", ""),
        tags=data.get("tags", []),
        scheduled_at=datetime_value,
        completed=data.get("completed", False),
    )
    
    items_store[item_id] = item
    
    # Update tags store
    for tag_name in item.tags:
        if tag_name not in tags_store:
            tags_store[tag_name] = Tag(name=tag_name)
    
    return jsonify(item.to_dict()), 201


@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    """Update an existing item."""
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    item = items_store[item_id]
    
    # Update fields
    if "title" in data:
        item.title = data["title"]
    if "details" in data:
        item.details = data.get("details", "")
    if "tags" in data:
        item.tags = data["tags"]
        # Update tags store
        for tag_name in item.tags:
            if tag_name not in tags_store:
                tags_store[tag_name] = Tag(name=tag_name)
    if "datetime" in data:
        if data["datetime"]:
            try:
                item.datetime = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                item.datetime = None
        else:
            item.datetime = None
    if "completed" in data:
        item.completed = data["completed"]
    if "type" in data:
        item.type = ItemType(data["type"])
    
    item.updated_at = datetime.now()
    
    return jsonify(item.to_dict())


@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item."""
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    del items_store[item_id]
    return jsonify({"message": "Item deleted"}), 200


@app.route("/api/items/<item_id>/toggle-complete", methods=["POST"])
def toggle_complete(item_id):
    """Toggle the completion status of an item."""
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    item = items_store[item_id]
    item.completed = not item.completed
    item.updated_at = datetime.now()
    
    return jsonify(item.to_dict())


# ==================== TAG ENDPOINTS ====================

@app.route("/api/tags", methods=["GET"])
def get_tags():
    """Get all tags."""
    return jsonify([tag.to_dict() for tag in tags_store.values()])


@app.route("/api/tags/<tag_name>", methods=["GET"])
def get_tag(tag_name):
    """Get a specific tag by name."""
    tag_name = tag_name.lower()
    if tag_name not in tags_store:
        return jsonify({"error": "Tag not found"}), 404
    return jsonify(tags_store[tag_name].to_dict())


@app.route("/api/tags/<tag_name>/items", methods=["GET"])
def get_items_by_tag(tag_name):
    """Get all items with a specific tag."""
    tag_name = tag_name.lower()
    items = [item for item in items_store.values() 
            if tag_name in [t.lower() for t in item.tags]]
    return jsonify([item.to_dict() for item in items])


# ==================== REMINDER ENDPOINTS ====================

@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    """
    Get all reminders, optionally filtered.
    Query parameters:
        - item_id: Filter by associated item ID
        - sent: Filter by sent status (true/false)
    """
    reminders = list(reminders_store.values())
    
    item_id = request.args.get("item_id")
    if item_id:
        reminders = [r for r in reminders if r.item_id == item_id]
    
    sent = request.args.get("sent")
    if sent is not None:
        sent_bool = sent.lower() == "true"
        reminders = [r for r in reminders if r.sent == sent_bool]
    
    return jsonify([reminder.to_dict() for reminder in reminders])


@app.route("/api/reminders/<reminder_id>", methods=["GET"])
def get_reminder(reminder_id):
    """Get a specific reminder by ID."""
    if reminder_id not in reminders_store:
        return jsonify({"error": "Reminder not found"}), 404
    return jsonify(reminders_store[reminder_id].to_dict())


@app.route("/api/reminders", methods=["POST"])
def create_reminder():
    """Create a new reminder."""
    data = request.get_json()
    
    if not data or not all(k in data for k in ["itemId", "telegramChatId", "scheduledTime"]):
        return jsonify({"error": "itemId, telegramChatId, and scheduledTime are required"}), 400
    
    # Verify item exists
    if data["itemId"] not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    reminder_id = data.get("id") or str(uuid.uuid4())
    
    try:
        scheduled_time = datetime.fromisoformat(data["scheduledTime"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return jsonify({"error": "Invalid scheduledTime format"}), 400
    
    reminder = Reminder(
        id=reminder_id,
        item_id=data["itemId"],
        telegram_chat_id=data["telegramChatId"],
        scheduled_time=scheduled_time,
        sent=data.get("sent", False),
    )
    
    reminders_store[reminder_id] = reminder
    return jsonify(reminder.to_dict()), 201


@app.route("/api/reminders/<reminder_id>", methods=["PUT"])
def update_reminder(reminder_id):
    """Update an existing reminder."""
    if reminder_id not in reminders_store:
        return jsonify({"error": "Reminder not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    reminder = reminders_store[reminder_id]
    
    if "telegramChatId" in data:
        reminder.telegram_chat_id = data["telegramChatId"]
    if "scheduledTime" in data:
        try:
            reminder.scheduled_time = datetime.fromisoformat(data["scheduledTime"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return jsonify({"error": "Invalid scheduledTime format"}), 400
    if "sent" in data:
        reminder.sent = data["sent"]
    
    return jsonify(reminder.to_dict())


@app.route("/api/reminders/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    """Delete a reminder."""
    if reminder_id not in reminders_store:
        return jsonify({"error": "Reminder not found"}), 404
    
    del reminders_store[reminder_id]
    return jsonify({"message": "Reminder deleted"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
