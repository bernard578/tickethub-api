from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict, Any

class Status(str, Enum):
    open = "open"
    closed = "closed"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Ticket(BaseModel):
    id: int
    title: str
    status: Status
    priority: Priority
    assignee: str
    description: Optional[str] = None

class TicketDetail(BaseModel):
    ticket: Ticket
    raw: Dict[str, Any]

class Stats(BaseModel):
    total: int
    by_status: Dict[str, int]
    by_priority: Dict[str, int]
