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

from app.models.comment_model import (
    TicketComment
)

from app.core.security import (
    get_current_user
)

from app.models.activity_log_model import (
    ActivityLog
)

from app.services.ai_classifier import (
    classify_ticket_ai, summarize_ticket, generate_ticket_response
)

from app.websockets.ticket_ws import (
    broadcast_ticket
)

from app.services.activity_logger import (
    log_activity
)

from datetime import (
    datetime,
    timedelta
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post(
    "/",
    response_model=TicketResponse
)
async def create_ticket(
    ticket: TicketCreate,
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        classification = (
            classify_ticket_ai(
                ticket.description
            )
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
            created_at=datetime.utcnow(),
            sla_deadline=sla_deadline,
            summary=summary,
            ai_response=ai_response,
        )

        db.add(new_ticket)

        db.commit()

        db.refresh(new_ticket)

        log_activity(
            db,
            f"Created ticket: {new_ticket.title}",
            user["username"]
        )

        asyncio.create_task(
            broadcast_ticket(
                "ticket_updated"
            )
        )

        return {
            "id": new_ticket.id,
            "title": new_ticket.title,
            "description": new_ticket.description,
            "priority": new_ticket.priority,
            "status": new_ticket.status,
            "sentiment": new_ticket.sentiment,
            "category": new_ticket.category,
            "assigned_to": new_ticket.assigned_to,
            "summary": new_ticket.summary,
            "created_at": new_ticket.created_at,
            "sla_deadline": new_ticket.sla_deadline,
            "ai_response": new_ticket.ai_response,
        }

    finally:

        db.close()


@router.get(
    "/",
    response_model=list[TicketResponse]
)
def get_tickets(
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        tickets = (
            db.query(Ticket).all()
        )

        return tickets

    finally:

        db.close()


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket_by_id(
    ticket_id: int,
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        ticket = (
            db.query(Ticket)
            .filter(
                Ticket.id == ticket_id
            )
            .first()
        )

        if not ticket:

            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        return ticket

    finally:

        db.close()


@router.get(
    "/{ticket_id}/activities"
)
def get_ticket_activities(
    ticket_id: int,
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        logs = (
            db.query(ActivityLog)
            .filter(
                ActivityLog.action.contains(
                    f"{ticket_id}"
                )
            )
            .order_by(
                ActivityLog.created_at.desc()
            )
            .all()
        )

        return logs

    finally:

        db.close()


@router.get(
    "/{ticket_id}/comments"
)
def get_ticket_comments(
    ticket_id: int,
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        comments = (
            db.query(TicketComment)
            .filter(
                TicketComment.ticket_id
                == ticket_id
            )
            .order_by(
                TicketComment.created_at.asc()
            )
            .all()
        )

        return comments

    finally:

        db.close()


@router.post(
    "/{ticket_id}/comments"
)
async def create_ticket_comment(
    ticket_id: int,
    content: str,
    user=Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        comment = TicketComment(
            ticket_id=ticket_id,
            username=user["username"],
            content=content,
            created_at=datetime.utcnow()
        )

        db.add(comment)

        db.commit()

        db.refresh(comment)

        log_activity(
            db,
            f"Added comment to ticket {ticket_id}",
            user["username"]
        )

        asyncio.create_task(
            broadcast_ticket(
                "ticket_updated"
            )
        )

        return comment

    finally:

        db.close()


@router.put("/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: int,
    status: str,
    user=Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail=
                "Not enough permissions"
        )

    db: Session = SessionLocal()

    try:

        ticket = (
            db.query(Ticket)
            .filter(
                Ticket.id == ticket_id
            )
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

        log_activity(
            db,
            (
                f"Changed status "
                f"of ticket "
                f"{ticket.id} "
                f"to {status}"
            ),
            user["username"]
        )

        asyncio.create_task(
            broadcast_ticket(
                "ticket_updated"
            )
        )

        return ticket

    finally:

        db.close()


@router.put("/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: int,
    assigned_to: str,
    user=Depends(get_current_user)
):

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail=
                "Not enough permissions"
        )

    db: Session = SessionLocal()

    try:

        ticket = (
            db.query(Ticket)
            .filter(
                Ticket.id == ticket_id
            )
            .first()
        )

        if not ticket:

            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )

        ticket.assigned_to = (
            assigned_to
        )

        db.commit()

        db.refresh(ticket)

        log_activity(
            db,
            (
                f"Assigned ticket "
                f"{ticket.id} "
                f"to {assigned_to}"
            ),
            user["username"]
        )

        asyncio.create_task(
            broadcast_ticket(
                "ticket_updated"
            )
        )

        return ticket

    finally:

        db.close()