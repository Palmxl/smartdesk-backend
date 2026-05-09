import asyncio

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.connection import (
    SessionLocal
)

from app.models.ticket_model import (
    Ticket
)

from app.services.websocket_manager import (
    manager
)

from app.schemas.ticket_schema import (
    TicketCreate,
    TicketResponse
)

from app.core.security import (
    get_current_user
)

from app.services.ai_classifier import (
    classify_ticket_ai, summarize_ticket, generate_ticket_response
)

from app.websockets.ticket_ws import (
    broadcast_ticket
)

from datetime import (
    datetime,
    timedelta
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    classification = classify_ticket_ai(
        ticket.description
    )

    summary = summarize_ticket(
        ticket.description
    )

    sla_deadline = (
        datetime.utcnow()
        + timedelta(hours=24)
    )

    ai_response = (
        generate_ticket_response(
            ticket.description
        )
    )
    
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=classification["priority"],
        sentiment=classification["sentiment"],
        category=classification["category"],
        created_at=datetime,
        sla_deadline=sla_deadline,
        summary=summary,
        ai_response=ai_response,
    )

    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)

    asyncio.create_task(
        broadcast_ticket(
            f"New ticket: {new_ticket.title}"
        )
    )

    asyncio.create_task(
        manager.broadcast(
            "ticket_updated"
        )
    )

    return new_ticket


@router.get("/", response_model=list[TicketResponse])
def get_tickets(
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    tickets = db.query(Ticket).all()

    return tickets


@router.put("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status: str,
    user=Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    db: Session = SessionLocal()

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.status = status

    db.commit()

    db.refresh(ticket)

    asyncio.create_task(
        manager.broadcast(
            "ticket_updated"
        )
    )

    return ticket

@router.put("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    assigned_to: str,
    user=Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    db: Session = SessionLocal()

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    ticket.assigned_to = assigned_to

    db.commit()

    db.refresh(ticket)

    return ticket