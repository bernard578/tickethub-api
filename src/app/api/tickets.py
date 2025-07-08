from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services import fetch_raw_todos, transform, get_user_map
from app.schemas import Ticket, TicketDetail
from app.schemas import Stats

router = APIRouter()

@router.get("/", response_model=List[Ticket])
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    q: Optional[str] = Query(None, alias="search"),
    skip: int = 0,
    limit: int = 10
) -> List[Ticket]:
    """
    Retrieve a list of tickets with optional filtering by status and priority,
    full-text search via 'search' alias, and pagination using skip & limit.
    """
    todos = await fetch_raw_todos()
    users = await get_user_map()
    tickets_list = [await transform(t, users) for t in todos]

    if status:
        tickets_list = [t for t in tickets_list if t.status.value == status]
    if priority:
        tickets_list = [t for t in tickets_list if t.priority.value == priority]
    if q:
        q_lower = q.lower()
        tickets_list = [
            t for t in tickets_list
            if q_lower in t.title.lower() or (t.description and q_lower in t.description.lower())
        ]

    return tickets_list[skip : skip + limit]

@router.get("/stats", response_model=Stats)
async def get_stats(
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> Stats:
    todos = await fetch_raw_todos()
    users = await get_user_map()
    tickets = [await transform(t, users) for t in todos]

    # apply filters
    if status:
        tickets = [t for t in tickets if t.status.value == status]
    if priority:
        tickets = [t for t in tickets if t.priority.value == priority]

    total = len(tickets)
    by_status = {}
    by_priority = {}
    for t in tickets:
        by_status[t.status.value] = by_status.get(t.status.value, 0) + 1
        by_priority[t.priority.value] = by_priority.get(t.priority.value, 0) + 1

    return Stats(total=total, by_status=by_status, by_priority=by_priority)
@router.get("/{ticket_id}", response_model=TicketDetail)
async def get_ticket(ticket_id: int) -> TicketDetail:
    """
    Retrieve a single ticket by ID, returning a TicketDetail containing both
    the transformed ticket and the raw JSON payload.
    """
    users = await get_user_map()
    todos = await fetch_raw_todos()
    todo = next((t for t in todos if t["id"] == ticket_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket = await transform(todo, users)
    return TicketDetail(ticket=ticket, raw=todo)


