from datetime import datetime
from typing import List, Optional
from enum import Enum


class ItemType(Enum):
    """Enumeration for item types."""
    NOTE = "note"
    REMINDER = "reminder"
    TASK = "task"


class Item:
    """
    Main entity class representing a note, reminder, or task.
    
    Attributes:
        id: Unique identifier for the item
        type: Type of item (note, reminder, or task)
        title: Title of the item
        details: Detailed description or content
        tags: List of tag names associated with the item
        datetime: Optional datetime for reminders and tasks
        completed: Whether the item is completed (for tasks and reminders)
        created_at: Timestamp when the item was created
        updated_at: Timestamp when the item was last updated
    """
    
    def __init__(
        self,
        id: str,
        type: ItemType,
        title: str,
        details: str = "",
        tags: Optional[List[str]] = None,
        scheduled_at: Optional[datetime] = None,
        completed: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.type = type if isinstance(type, ItemType) else ItemType(type)
        self.title = title
        self.details = details
        self.tags = tags if tags is not None else []
        self.datetime = scheduled_at
        self.completed = completed
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
    
    def to_dict(self) -> dict:
        """Convert the item to a dictionary representation."""
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "details": self.details,
            "tags": self.tags,
            "datetime": self.datetime.isoformat() if self.datetime else None,
            "completed": self.completed,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Item':
        """Create an Item instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            type=ItemType(data.get("type", "note")),
            title=data.get("title", ""),
            details=data.get("details", ""),
            tags=data.get("tags", []),
            scheduled_at=datetime.fromisoformat(data["datetime"]) if data.get("datetime") else None,
            completed=data.get("completed", False),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None,
            updated_at=datetime.fromisoformat(data["updatedAt"]) if data.get("updatedAt") else None,
        )


class User:
    """
    Entity class representing an application user.

    Attributes:
        id: Unique identifier for the user
        name: Display name or username
        email: Optional email address for account or notification purposes
        telegram_chat_id: Optional Telegram chat ID for reminders
        timezone: Optional IANA timezone string for scheduling
        created_at: Timestamp when the user record was created
        updated_at: Timestamp when the user record was last updated
    """

    def __init__(
        self,
        id: str,
        name: str,
        email: Optional[str] = None,
        telegram_chat_id: Optional[str] = None,
        timezone: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name.strip()
        self.email = email.lower().strip() if email else None
        self.telegram_chat_id = telegram_chat_id
        self.timezone = timezone
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()

    def to_dict(self) -> dict:
        """Convert the user to a dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "telegramChatId": self.telegram_chat_id,
            "timezone": self.timezone,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create a User instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            telegram_chat_id=data.get("telegramChatId"),
            timezone=data.get("timezone"),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None,
            updated_at=datetime.fromisoformat(data["updatedAt"]) if data.get("updatedAt") else None,
        )


class Tag:
    """
    Entity class representing a tag for categorizing items.
    
    Attributes:
        name: Name of the tag (unique identifier)
        color: Optional color code for visual representation
        created_at: Timestamp when the tag was first created
    """
    
    def __init__(
        self,
        name: str,
        color: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.name = name.lower().strip()  # Normalize tag names
        self.color = color
        self.created_at = created_at if created_at is not None else datetime.now()
    
    def to_dict(self) -> dict:
        """Convert the tag to a dictionary representation."""
        return {
            "name": self.name,
            "color": self.color,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tag':
        """Create a Tag instance from a dictionary."""
        return cls(
            name=data.get("name", ""),
            color=data.get("color"),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None,
        )


class Reminder:
    """
    Entity class representing a Telegram reminder notification.
    This is separate from the Item type 'reminder' and represents
    the actual notification mechanism.
    
    Attributes:
        id: Unique identifier for the reminder
        item_id: ID of the associated item
        telegram_chat_id: Telegram chat ID to send the reminder to
        scheduled_time: When the reminder should be sent
        sent: Whether the reminder has been sent
        created_at: Timestamp when the reminder was created
    """
    
    def __init__(
        self,
        id: str,
        item_id: str,
        telegram_chat_id: str,
        scheduled_time: datetime,
        sent: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.item_id = item_id
        self.telegram_chat_id = telegram_chat_id
        self.scheduled_time = scheduled_time
        self.sent = sent
        self.created_at = created_at if created_at is not None else datetime.now()
    
    def to_dict(self) -> dict:
        """Convert the reminder to a dictionary representation."""
        return {
            "id": self.id,
            "itemId": self.item_id,
            "telegramChatId": self.telegram_chat_id,
            "scheduledTime": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "sent": self.sent,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reminder':
        """Create a Reminder instance from a dictionary."""
        return cls(
            id=data.get("id", ""),
            item_id=data.get("itemId", ""),
            telegram_chat_id=data.get("telegramChatId", ""),
            scheduled_time=datetime.fromisoformat(data["scheduledTime"]) if data.get("scheduledTime") else None,
            sent=data.get("sent", False),
            created_at=datetime.fromisoformat(data["createdAt"]) if data.get("createdAt") else None,
        )

