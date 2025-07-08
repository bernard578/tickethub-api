import pytest
from app.schemas import Ticket, TicketDetail, Status, Priority

def test_list_tickets_default(client):
    response = client.get("/tickets/")
    assert response.status_code == 200
    tickets = [Ticket(**item) for item in response.json()]
    assert isinstance(tickets, list)
    # With 3 mocked todos, default limit 10 returns all 3
    assert len(tickets) == 3


def test_get_ticket_success(client):
    response = client.get("/tickets/1")
    assert response.status_code == 200
    data = response.json()

    ticket_detail = TicketDetail(**data)
    ticket = ticket_detail.ticket
    raw = ticket_detail.raw

    assert ticket.id == raw["id"]
    assert ticket.title == raw["todo"]
    assert ticket.status in {Status.open, Status.closed}
    assert ticket.priority in {Priority.low, Priority.medium, Priority.high}
    assert raw["userId"] == 42


def test_get_ticket_not_found(client):
    response = client.get("/tickets/9999")
    assert response.status_code == 404


def test_filter_status(client):
    response = client.get("/tickets/?status=open")
    assert response.status_code == 200
    tickets = [Ticket(**item) for item in response.json()]
    # Both IDs 1 and 3 are open (completed=False)
    assert {t.id for t in tickets} == {1, 3}


def test_search_query(client):
    response = client.get("/tickets/?search=Buy")
    assert response.status_code == 200
    tickets = [Ticket(**item) for item in response.json()]
    assert len(tickets) == 1
    assert tickets[0].title == "Buy milk"


def test_pagination(client):
    res1 = client.get("/tickets/?skip=0&limit=2")
    res2 = client.get("/tickets/?skip=2&limit=2")
    assert res1.status_code == 200 and res2.status_code == 200
    d1 = [Ticket(**item) for item in res1.json()]
    d2 = [Ticket(**item) for item in res2.json()]

    assert len(d1) == 2
    assert len(d2) == 1
    assert {t.id for t in d1}.isdisjoint({t.id for t in d2})