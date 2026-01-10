from datetime import datetime
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, default="")
    tags = db.Column(ARRAY(db.String), default=list)
    telegram_id = db.Column(db.String(64))
    deadline = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "details": self.details or "",
            "tags": self.tags or [],
            "telegramChatId": self.telegram_id,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed": self.completed,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


class Tag(db.Model):
    __tablename__ = "tags"

    name = db.Column(db.String(100), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {"name": self.name, "createdAt": self.created_at.isoformat() if self.created_at else None}


class Reminder(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, default="")
    tags = db.Column(ARRAY(db.String), default=list)
    telegram_id = db.Column(db.String(64), nullable=False)
    scheduled_at = db.Column(db.DateTime)
    sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "details": self.details or "",
            "tags": self.tags or [],
            "telegramChatId": self.telegram_id,
            "scheduledTime": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "sent": self.sent,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }



def parse_dt(value: Optional[str]):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None
    
    
