from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from databases import Database
import os
from dotenv import load_dotenv
from sqlalchemy import String, DateTime, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .models import NotificationStatus

class Base(DeclarativeBase):
    pass
class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status_message: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(Enum(NotificationStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

load_dotenv()


DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_HOST")
DATABASE_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

database = Database(DATABASE_URL)

if __name__ == "__main__":
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)