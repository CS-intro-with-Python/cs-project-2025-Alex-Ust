from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from models import Item, ItemType, Tag, Reminder, parse_dt

app = Flask(__name__)

# In-memory storage
items_store = {}
tags_store = {}
reminders_store = {}
item_counter = 0
reminder_counter = 0

#==================== Counter + Maker ====================
def new_item_id():
    global item_counter
    item_counter += 1
    return str(item_counter)


def new_reminder_id():
    global reminder_counter
    reminder_counter += 1
    return str(reminder_counter)


def tag_list(raw):
    return [t.strip().lower() for t in (raw or "").split(",") if t.strip()]


def update_tags(tags):
    for tag_name in tags:
        tags_store.setdefault(tag_name, Tag(name=tag_name))


def build_item(data, existing=None):
    """Create or update Item from dict/form data."""
    item = existing or Item(
        id=data.get("id") or new_item_id(),
        type=ItemType(data.get("type", "task")),
        title="",
    )
    item.title = (data.get("title") or "").strip()
    item.details = data.get("details", "") or ""
    item.tags = tag_list(data.get("tags", ""))
    item.telegram_chat_id = data.get("telegramChatId")

    # set type if provided
    if "type" in data:
        item.type = ItemType(data.get("type", item.type.value))

    if item.type == ItemType.REMINDER:
        item.scheduled_at = parse_dt(data.get("datetime"))
        item.deadline = None
    else:
        item.deadline = parse_dt(data.get("deadline"))
        item.scheduled_at = None
    if "completed" in data:
        item.completed = bool(data.get("completed"))
    item.updated_at = datetime.now()
    update_tags(item.tags)
    return item


@app.route("/")
def hello():
    """Main page with items list."""
    filter_type = request.args.get("type", "all")
    filter_tag = request.args.get("tag", "all")
    search_query = request.args.get("search", "")
    
    items = list(items_store.values())
    
    if filter_type != "all":
        items = [item for item in items if item.type.value == filter_type]
    if filter_tag != "all":
        items = [item for item in items if filter_tag.lower() in [t.lower() for t in item.tags]]
    if search_query:
        search_lower = search_query.lower()
        items = [item for item in items 
                if search_lower in item.title.lower() or search_lower in item.details.lower()]
    
    reminders = [item for item in items if item.type == ItemType.REMINDER]
    tasks = [item for item in items if item.type == ItemType.TASK]
    
    reminders.sort(key=lambda x: (x.scheduled_at or datetime.min, x.created_at))
    tasks.sort(key=lambda x: (x.deadline or datetime.min, x.created_at))
    
    all_tags = sorted(set(tag.lower() for item in items_store.values() for tag in item.tags))
    
    counts = {
        "reminder": len([i for i in items_store.values() if i.type == ItemType.REMINDER]),
        "task": len([i for i in items_store.values() if i.type == ItemType.TASK]),
    }
    
    return render_template(
        "index.html",
        reminders=reminders,
        tasks=tasks,
        all_tags=all_tags,
        counts=counts,
        filter_type=filter_type,
        filter_tag=filter_tag,
        search_query=search_query,
    )


# ==================== ITEM ENDPOINTS ====================

@app.route("/api/items", methods=["GET"])
def get_items():
    items = list(items_store.values())
    t = request.args.get("type")
    tag = request.args.get("tag")
    search = (request.args.get("search") or "").lower()
    completed = request.args.get("completed")

    if t:
        items = [i for i in items if i.type.value == t]
    if tag:
        items = [i for i in items if tag.lower() in [t.lower() for t in i.tags]]
    if search:
        items = [i for i in items if search in i.title.lower() or search in i.details.lower()]
    if completed is not None:
        want = completed.lower() == "true"
        items = [i for i in items if i.completed == want]
    return jsonify([i.to_dict() for i in items])


@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id):
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(items_store[item_id].to_dict())


@app.route("/items/create", methods=["POST"])
def create_item_form():
    data = request.form
    if not (data.get("title") or "").strip():
        return redirect(url_for("hello") + "?error=Title is required")
    item = build_item(data)
    if not item.title:
        return redirect(url_for("hello") + "?error=Title is required")
    items_store[item.id] = item
    return redirect(url_for("hello"))


@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    data.setdefault("id", new_item_id())
    item = build_item(data)
    items_store[item.id] = item
    return jsonify(item.to_dict()), 201


@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json() or {}
    updated = build_item(data, existing=items_store[item_id])
    items_store[item_id] = updated
    return jsonify(updated.to_dict())


@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    del items_store[item_id]
    return jsonify({"message": "Item deleted"}), 200


@app.route("/items/<item_id>/toggle-complete", methods=["POST"])
def toggle_complete_form(item_id):
    if item_id not in items_store:
        return redirect(url_for("hello") + "?error=Item not found")
    
    item = items_store[item_id]
    item.completed = not item.completed
    item.updated_at = datetime.now()
    
    return redirect(url_for("hello"))


@app.route("/items/<item_id>/edit", methods=["GET"])
def edit_item_form(item_id):
    if item_id not in items_store:
        return redirect(url_for("hello") + "?error=Item not found")
    
    item = items_store[item_id]
    
    filter_type = request.args.get("type", "all")
    filter_tag = request.args.get("tag", "all")
    search_query = request.args.get("search", "")
    
    items = list(items_store.values())
    reminders = [i for i in items if i.type == ItemType.REMINDER]
    tasks = [i for i in items if i.type == ItemType.TASK]
    all_tags = sorted(set(tag.lower() for item in items_store.values() for tag in item.tags))
    counts = {
        "reminder": len([i for i in items_store.values() if i.type == ItemType.REMINDER]),
        "task": len([i for i in items_store.values() if i.type == ItemType.TASK]),
    }
    
    return render_template(
        "index.html",
        reminders=reminders,
        tasks=tasks,
        all_tags=all_tags,
        counts=counts,
        filter_type=filter_type,
        filter_tag=filter_tag,
        search_query=search_query,
        edit_item=item,
    )


@app.route("/items/<item_id>/update", methods=["POST"])
def update_item_form(item_id):
    if item_id not in items_store:
        return redirect(url_for("hello") + "?error=Item not found")
    
    items_store[item_id] = build_item(request.form, existing=items_store[item_id])
    return redirect(url_for("hello"))


@app.route("/items/<item_id>/delete", methods=["POST"])
def delete_item_form(item_id):
    if item_id not in items_store:
        return redirect(url_for("hello") + "?error=Item not found")
    
    del items_store[item_id]
    return redirect(url_for("hello"))


@app.route("/api/items/<item_id>/toggle-complete", methods=["POST"])
def toggle_complete(item_id):
    if item_id not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    item = items_store[item_id]
    item.completed = not item.completed
    item.updated_at = datetime.now()
    
    return jsonify(item.to_dict())


# ==================== TAG ENDPOINTS ====================

@app.route("/api/tags", methods=["GET"])
def get_tags():
    return jsonify([tag.to_dict() for tag in tags_store.values()])


@app.route("/api/tags/<tag_name>", methods=["GET"])
def get_tag(tag_name):
    tag_name = tag_name.lower()
    if tag_name not in tags_store:
        return jsonify({"error": "Tag not found"}), 404
    return jsonify(tags_store[tag_name].to_dict())


@app.route("/api/tags/<tag_name>/items", methods=["GET"])
def get_items_by_tag(tag_name):
    tag_name = tag_name.lower()
    items = [item for item in items_store.values() 
            if tag_name in [t.lower() for t in item.tags]]
    return jsonify([item.to_dict() for item in items])


# ==================== REMINDER ENDPOINTS ====================

@app.route("/api/reminders", methods=["GET"])
def get_reminders():
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
    if reminder_id not in reminders_store:
        return jsonify({"error": "Reminder not found"}), 404
    return jsonify(reminders_store[reminder_id].to_dict())


@app.route("/api/reminders", methods=["POST"])
def create_reminder():
    data = request.get_json()
    
    if not data or not all(k in data for k in ["itemId", "telegramChatId"]):
        return jsonify({"error": "itemId and telegramChatId are required"}), 400
    
    if data["itemId"] not in items_store:
        return jsonify({"error": "Item not found"}), 404
    
    reminder_id = data.get("id") or new_reminder_id()
    
    scheduled_time = parse_dt(data.get("scheduledTime"))
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
    if reminder_id not in reminders_store:
        return jsonify({"error": "Reminder not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    reminder = reminders_store[reminder_id]
    
    if "telegramChatId" in data:
        reminder.telegram_chat_id = data["telegramChatId"]
    if "scheduledTime" in data:
        reminder.scheduled_time = parse_dt(data.get("scheduledTime"))
    if "sent" in data:
        reminder.sent = data["sent"]
    
    return jsonify(reminder.to_dict())


@app.route("/api/reminders/<reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    if reminder_id not in reminders_store:
        return jsonify({"error": "Reminder not found"}), 404
    
    del reminders_store[reminder_id]
    return jsonify({"message": "Reminder deleted"}), 200





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
