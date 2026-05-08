from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.ticket_model import Ticket

from app.schemas.ticket_schema import (
    TicketCreate,
    TicketResponse
)

from app.services.ticket_classifier import (
    classify_ticket
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post("/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):

    db: Session = SessionLocal()

    classification = classify_ticket(
        ticket.description
    )

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=classification["priority"],
        sentiment=classification["sentiment"],
        category=classification["category"],
    )

    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)

    return new_ticket


@router.get("/", response_model=list[TicketResponse])
def get_tickets():

    db: Session = SessionLocal()

    tickets = db.query(Ticket).all()

    return tickets

@router.put("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status: str
):

    db: Session = SessionLocal()

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    ticket.status = status

    db.commit()

    db.refresh(ticket)

    return ticket