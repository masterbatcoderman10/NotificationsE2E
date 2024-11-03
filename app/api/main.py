from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class StatusUpdate(BaseModel):
    status: str

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status")
def get_status():
    return {"status" : "all is well"}

@app.post("/status")
def post_status(status_update: StatusUpdate):
    return {"message" : f"status updated to {status_update.status}"}