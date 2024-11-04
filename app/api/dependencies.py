# tasks.py
from celery import Celery
import os
from dotenv import load_dotenv
import asyncio
from .db import database
from .crud import create_notification

load_dotenv()

BROKER_HOST = os.getenv("BROKER_HOST")

celery = Celery('tasks', broker=f'pyamqp://guest@{BROKER_HOST}//')

def run_async(coro):
    """Helper function to run async code in celery task"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@celery.task
def create_notification_task(message: str):
    # Connect to database
    run_async(database.connect())
    
    try:
        # Create the notification
        result = run_async(
            create_notification(message=message)
        )
        return result
    finally:
        # Ensure we close the database connection
        run_async(database.disconnect())