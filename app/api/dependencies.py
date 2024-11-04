from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

BROKER_HOST = os.getenv("BROKER_HOST")

celery = Celery('tasks', broker=f'pyamqp://guest@{BROKER_HOST}//')

@celery.task
def create_get_notification():
    return {"message" : "notification retrieved"}

@celery.task
def create_post_notification():
    return {"message" : "notification created"}