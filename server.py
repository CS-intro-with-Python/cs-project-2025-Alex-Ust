import os
import logging 
import logger
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Task, Reminder, parse_dt
import time

app = Flask(__name__)

# logger setup for requersts including method, path, client IP
@app.before_request
def load_user():
    logger = logging.getLogger("app_logger")
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    logger.info("Incoming request: %s %s from %s", request.method, request.path, client_ip)
    logger.info("Happy new year 2026!")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:mysecretpassword@host.docker.internal:5432/items_storage",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



logger.setup_logger() 




def build_task(data, existing: Task | None = None):
    task = existing or Task()
    task.title = (data.get("title") or "").strip()
    task.details = data.get("details", "") or ""
    task.deadline = parse_dt(data.get("deadline") or data.get("datetime"))
    if "completed" in data:
        task.completed = bool(data.get("completed"))
    task.updated_at = datetime.now()
    return task


def build_reminder(data, existing: Reminder | None = None):
    reminder = existing or Reminder()
    reminder.title = (data.get("title") or "").strip()
    reminder.details = data.get("details", "") or ""
    reminder.scheduled_at = parse_dt(data.get("scheduledTime")) or parse_dt(data.get("datetime"))
    if "sent" in data:
        reminder.sent = bool(data.get("sent"))
    reminder.updated_at = datetime.now()
    return reminder


#Checking DB connection, for github else client cannot connect to localhost:8080 
with app.app_context():
    for attempt in range(10):
        try:
            db.create_all()
            break
        except Exception:
            if attempt == 9:
                raise
            time.sleep(2)




@app.route("/")
def hello():
    filter_type = request.args.get("type", "all")

    reminders = (Reminder.query.order_by(Reminder.scheduled_at, Reminder.created_at).all() if filter_type != "task" else [])

    tasks = (Task.query.order_by(Task.deadline, Task.created_at).all() if filter_type != "reminder" else [])
    
    counts = {"reminder": Reminder.query.count(), "task": Task.query.count()}

    return render_template("index.html", reminders=reminders, tasks=tasks, counts=counts, filter_type=filter_type)


@app.route("/tasks/create", methods=["POST"])
def create_task_form():
    data = request.form
    if not (data.get("title") or "").strip():
        return redirect(url_for("hello") + "?error=Title is required")
    if data.get("type") == "reminder":
        item = build_reminder(data)
    else:
        item = build_task(data)
    item.created_at = datetime.now()
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("hello"))


@app.route("/tasks/<int:task_id>/edit")
def edit_task_form(task_id):
    item = Task.query.get(task_id)
    if not item:
        return redirect(url_for("hello") + "?error=Item not found")

    edit_target = item
    edit_type = "task"
    filter_type = request.args.get("type", "all")

    reminders = Reminder.query.all()
    tasks = Task.query.all()
    counts = {
        "reminder": Reminder.query.count(),
        "task": Task.query.count(),
    }

    return render_template(
        "index.html",
        reminders=reminders,
        tasks=tasks,
        counts=counts,
        filter_type=filter_type,
        edit_item=edit_target,
        edit_type=edit_type,
    )


@app.route("/tasks/<int:task_id>/update", methods=["POST"])
def update_task_form(task_id):
    item = Task.query.get(task_id)
    if not item:
        return redirect(url_for("hello") + "?error=Item not found")
    data = request.form
    build_task(data, existing=item)
    db.session.commit()
    return redirect(url_for("hello"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task_form(task_id):
    item = Task.query.get(task_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("hello"))


@app.route("/tasks/<int:task_id>/if-complete", methods=["POST"])
def toggle_task_complete_form(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        task.updated_at = datetime.now()
        db.session.commit()
    return redirect(url_for("hello"))


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    query = Task.query
    completed = request.args.get("completed")

    if completed is not None:
        query = query.filter(Task.completed == (completed.lower() == "true"))
    return jsonify([i.to_dict() for i in query.all()])


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    item = Task.query.get(task_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict())


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400
    item = build_task(data)
    item.created_at = datetime.now()
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json() or {}
    build_task(data, existing=task)
    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    item = Task.query.get(task_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200


@app.route("/api/tasks/<int:task_id>/if-complete", methods=["POST"])
def toggle_task_complete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Item not found"}), 404
    task.completed = not task.completed
    task.updated_at = datetime.now()
    db.session.commit()
    return jsonify(task.to_dict())

#========================================REMINDERS================================================#
@app.route("/reminders/create", methods=["POST"])
def create_reminder_form():
    data = request.form
    if not (data.get("title") or "").strip():
        return redirect(url_for("hello") + "?error=Title is required")
    reminder = build_reminder(data)
    reminder.created_at = datetime.now()
    db.session.add(reminder)
    db.session.commit()
    return redirect(url_for("hello"))


@app.route("/reminders/<int:reminder_id>/edit")
def edit_reminder_form(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return redirect(url_for("hello") + "?error=Reminder not found")

    filter_type = request.args.get("type", "all")
    reminders = Reminder.query.all()
    tasks = Task.query.all()
    counts = {
        "reminder": Reminder.query.count(),
        "task": Task.query.count(),
    }

    return render_template(
        "index.html",
        reminders=reminders,
        tasks=tasks,
        counts=counts,
        filter_type=filter_type,
        edit_item=reminder,
        edit_type="reminder",
    )


@app.route("/reminders/<int:reminder_id>/update", methods=["POST"])
def update_reminder_form(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return redirect(url_for("hello") + "?error=Reminder not found")
    data = request.form
    build_reminder(data, existing=reminder)
    db.session.commit()
    return redirect(url_for("hello"))


@app.route("/reminders/<int:reminder_id>/delete", methods=["POST"])
def delete_reminder_form(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
    return redirect(url_for("hello"))


@app.route("/reminders/<int:reminder_id>/if-complete", methods=["POST"])
def toggle_reminder_complete_form(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if reminder:
        reminder.sent = not reminder.sent
        reminder.updated_at = datetime.now()
        db.session.commit()
    return redirect(url_for("hello"))


@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    query = Reminder.query
    item_id = request.args.get("item_id")
    sent = request.args.get("sent")
    if sent is not None:
        query = query.filter_by(sent=(sent.lower() == "true"))
    return jsonify([r.to_dict() for r in query.all()])


@app.route("/api/reminders/<int:reminder_id>", methods=["GET"])
def get_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
    return jsonify(reminder.to_dict())


@app.route("/api/reminders", methods=["POST"])
def create_reminder():
    data = request.get_json() or {}
    if not data.get("title"):
        return jsonify({"error": "title is required"}), 400
    reminder = Reminder(
        title=data["title"],
        details=data.get("details", ""),
        scheduled_at=parse_dt(data.get("scheduledTime")),
        sent=bool(data.get("sent", False)),
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify(reminder.to_dict()), 201


@app.route("/api/reminders/<int:reminder_id>", methods=["PUT"])
def update_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
    data = request.get_json() or {}
    if "title" in data:
        reminder.title = data["title"].strip()
    if "details" in data:
        reminder.details = data.get("details", "")
    if "scheduledTime" in data:
        reminder.scheduled_at = parse_dt(data.get("scheduledTime"))
    if "sent" in data:
        reminder.sent = bool(data["sent"])
    reminder.updated_at = datetime.now()
    db.session.commit()
    return jsonify(reminder.to_dict())


@app.route("/api/reminders/<int:reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder deleted"}), 200


@app.route("/api/reminders/<int:reminder_id>/if-complete", methods=["POST"])
def toggle_reminder_complete(reminder_id):
    reminder = Reminder.query.get(reminder_id)
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
    reminder.sent = not reminder.sent
    reminder.updated_at = datetime.now()
    db.session.commit()
    return jsonify(reminder.to_dict())

@app.route("/relax")
def relax():
    return render_template("relax.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
