from sqlalchemy import insert, select, update
from .db import database, Status, Notification
from .models import NotificationStatus
from datetime import datetime, timedelta

def format_time_since(time_since: timedelta) -> str:
    """
    Format time since notification was created in human readable format
    """

    total_seconds = int(time_since.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds}s +"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes}m +"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours}h +"
    elif total_seconds < 2592000:
        days = total_seconds // 86400
        return f"{days}d +"
    else:
        return "1m +"

async def create_status(status_message: str) -> dict:

    stmt = insert(Status).values(
        status_message=status_message, created_at=datetime.utcnow())

    try:
        await database.execute(stmt)
        return {"message": "status created"}
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

    stmt = insert(Notification).values(
        message=message, status=NotificationStatus.UNREAD, created_at=datetime.utcnow()
    ).returning(Notification.id)

    try:
        notification_id = await database.execute(stmt)
        return {"message": "notification created", "id": notification_id}
    except Exception as e:
        raise e


from datetime import datetime
from sqlalchemy import select

async def get_notification_crud() -> Notification:
    """
    Get's most recent unread and read notifications.
    """

    unread_stmt = select(
        Notification.id,
        Notification.message,
        Notification.created_at
    ).where(
        Notification.status == NotificationStatus.UNREAD
    ).order_by(
        Notification.created_at.desc()
    )
    
    read_stmt = select(
        Notification.id,
        Notification.message,
        Notification.created_at
    ).where(
        Notification.status == NotificationStatus.READ
    ).order_by(
        Notification.created_at.desc()
    )

    try:
        unread = await database.fetch_all(unread_stmt)
        read = await database.fetch_all(read_stmt)

        formatted_unread = [
            {
                "id": row.id,
                "message": row.message,
                "time_since": format_time_since(datetime.utcnow() - row.created_at)
            }
            for row in unread
        ]

        formatted_read = [
            {
                "id": row.id,
                "message": row.message,
                "time_since": format_time_since(datetime.utcnow() - row.created_at)
            }
            for row in read
        ]

        return {"unread": formatted_unread, "read": formatted_read}
    except Exception as e:
        raise e


async def update_notification_crud(notification_id: int) -> dict:

    stmt = update(Notification).where(
        Notification.id == notification_id).values(status=NotificationStatus.READ)

    try:
        await database.execute(stmt)
        return {"message": "notification updated"}
    except Exception as e:
        raise e
