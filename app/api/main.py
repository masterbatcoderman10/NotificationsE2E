from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .db import database
from .dependencies import create_notification_task, web_socket_manager
from .crud import get_status_crud, create_status, create_notification, get_notification_crud, update_notification_crud

class StatusUpdate(BaseModel):
    status: str

class Notification(BaseModel):
    id: int
    message: str
    time_since: str
class NotificationsResponse(BaseModel):
    unread: List[Notification]
    read: List[Notification]

app = FastAPI()

origins = [
    #localhost 5173
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

# shutdown event
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Modified API endpoints
@app.get("/status")
async def get_status():
    create_notification_task.delay("Status requested")
    return await get_status_crud()

@app.post("/status")
async def post_status(status_update: StatusUpdate):
    create_notification_task.delay(f"Status updated to {status_update.status}")
    return await create_status(status_update.status)

@app.get("/notifications", response_model=NotificationsResponse)
async def get_notifications():
    
    notifications = await get_notification_crud()

    return NotificationsResponse(
        unread=notifications["unread"],
        read=notifications["read"]
    )

@app.patch("/notifications/{notification_id}")
async def update_notification(notification_id: int):
    return await update_notification_crud(notification_id=notification_id)

# Websocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await web_socket_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await web_socket_manager.send_personal_message({"message": data}, user_id)
    except:
        web_socket_manager.disconnect(user_id)