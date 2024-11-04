from sqlalchemy import insert, select
from .db import database, Status, Notification
from .models import NotificationStatus
from datetime import datetime

async def create_status(status_message: str) -> dict:

    stmt = insert(Status).values(status_message=status_message, created_at=datetime.utcnow())

    try:
        await database.execute(stmt)
        return {"message" : "status created"}
    except Exception as e:
        raise e

async def get_status_crud() -> Status:
    """
    Get's most recent status message
    """

    stmt = select(Status).order_by(Status.created_at.desc()).limit(1)

    try:
        return await database.fetch_one(stmt)
    except Exception as e:
        raise e

async def create_notification(message: str) -> dict:

    stmt = insert(Notification).values(message=message, status=NotificationStatus.UNREAD, created_at=datetime.utcnow())

    try:
        await database.execute(stmt)
        return {"message" : "notification created"}
    except Exception as e:
        raise e

