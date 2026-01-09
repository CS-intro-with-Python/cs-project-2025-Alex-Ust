from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Optional


class ItemType(Enum):
  REMINDER = "reminder"
  TASK = "task"


def parse_dt(value: Optional[str]) -> Optional[datetime]:
  if not value:
    return None
  try:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
  except Exception:
    return None


@dataclass
class Item:
  id: str
  type: ItemType
  title: str
  details: str = ""
  tags: List[str] = field(default_factory=list)
  telegram_chat_id: Optional[str] = None
  scheduled_at: Optional[datetime] = None
  deadline: Optional[datetime] = None
  completed: bool = False
  created_at: datetime = field(default_factory=datetime.now)
  updated_at: datetime = field(default_factory=datetime.now)

  def to_dict(self) -> dict:
    data = asdict(self)
    data["type"] = self.type.value
    data["createdAt"] = self.created_at.isoformat()
    data["updatedAt"] = self.updated_at.isoformat()
    data["datetime"] = self.scheduled_at.isoformat() if self.scheduled_at else None
    data["deadline"] = self.deadline.isoformat() if self.deadline else None
    data["telegramChatId"] = self.telegram_chat_id
    data.pop("scheduled_at", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    return data

  @classmethod
  def from_payload(cls, data: dict) -> "Item":
    kind = ItemType(data.get("type", "task"))
    return cls(
      id=data.get("id", ""),
      type=kind,
      title=data.get("title", "").strip(),
      details=data.get("details", "") or "",
      tags=data.get("tags", []) or [],
      telegram_chat_id=data.get("telegramChatId"),
      scheduled_at=parse_dt(data.get("datetime")) if kind == ItemType.REMINDER else None,
      deadline=parse_dt(data.get("deadline")) if kind == ItemType.TASK else None,
      completed=bool(data.get("completed", False)),
      created_at=parse_dt(data.get("createdAt")) or datetime.now(),
      updated_at=parse_dt(data.get("updatedAt")) or datetime.now(),
    )


@dataclass
class Tag:
  name: str
  color: Optional[str] = None
  created_at: datetime = field(default_factory=datetime.now)

  def to_dict(self) -> dict:
    return {"name": self.name, "color": self.color, "createdAt": self.created_at.isoformat()}


@dataclass
class Reminder:
  id: str
  item_id: str
  telegram_chat_id: str
  scheduled_time: Optional[datetime] = None
  sent: bool = False
  created_at: datetime = field(default_factory=datetime.now)

  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "itemId": self.item_id,
      "telegramChatId": self.telegram_chat_id,
      "scheduledTime": self.scheduled_time.isoformat() if self.scheduled_time else None,
      "sent": self.sent,
      "createdAt": self.created_at.isoformat() if self.created_at else None,
    }
