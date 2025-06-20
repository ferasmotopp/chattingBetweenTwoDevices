from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Message
from schemas import MessageCreate
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/messages/")
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message)

@app.get("/messages/{sender_id}/{receiver_id}")
def get_messages(sender_id: int, receiver_id: int, db: Session = Depends(get_db)):
    return crud.get_messages_between_users(db, sender_id, receiver_id)
