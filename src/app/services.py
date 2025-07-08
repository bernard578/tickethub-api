import httpx
from app.schemas import Ticket, Status, Priority

BASE = "https://dummyjson.com"

async def fetch_raw_todos():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE}/todos")
        resp.raise_for_status()
        return resp.json()["todos"]

async def transform(todo: dict, user_map: dict) -> Ticket:
    status = Status.closed if todo.get("completed") else Status.open
    pri = [Priority.low, Priority.medium, Priority.high][todo.get("id") % 3]
    assignee = user_map.get(todo.get("userId"), "unknown")
    return Ticket(
    id=todo["id"],
    title=todo["todo"],
    status=status,
    priority=pri,
    assignee=assignee,
    description=todo.get("todo")[:100]
    )

async def get_user_map():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE}/users")
        resp.raise_for_status()
        users = resp.json()["users"]
        return {u["id"]: u["username"] for u in users}