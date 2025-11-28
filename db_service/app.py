from fastapi import FastAPI, Depends
from database import SessionLocal, init_db
import crud
from schemas import MailCreate, AnswerCreate

init_db()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/mails")
def get_mails(db=Depends(get_db)):
    return crud.get_all_mails(db)

@app.get("/api/mails/{mail_id}")
def get_mail(mail_id: str, db=Depends(get_db)):
    return crud.get_mail(db, mail_id)

@app.post("/api/customers/{customer_id}/mail")
def create_mail(customer_id: str, mail: MailCreate, db=Depends(get_db)):
    return crud.create_mail(db, customer_id, mail)

@app.post("/api/mails/{mail_id}/answer")
def create_answer(mail_id: str, answer: AnswerCreate, db=Depends(get_db)):
    return crud.create_answer(db, mail_id, answer)
