from fastapi import FastAPI
from threading import Thread
from schemas import MailIn, CustomerIn
import mq
import db_client
import json

app = FastAPI()


@app.get("/bank/mails")
def list_mails():
    return db_client.get_all_mails()

@app.get("/bank/mails/{mail_id}")
def get_mail(mail_id: str):
    return db_client.get_mail(mail_id)

@app.post("/bank/mails")
def create_mail(mail_in: MailIn):
    mail = db_client.save_mail(mail_in.customerId, mail_in.mailText)
    mq.publish_ai_request(mail["uuid"], mail_in.mailText)
    return {"status": "queued", "mail": mail}

@app.get("/bank/customers")
def list_customers():
    return db_client.get_customers()

@app.post("/bank/customers")
def create_customer_route(customer: CustomerIn):
    return db_client.create_customer(customer.name, customer.personType)

def ai_response_callback(ch, method, properties, body):
    data = json.loads(body)
    mail_id = data["mail_id"]
    answer_text = data["answer_text"]
    is_important = data.get("is_important", False)
    is_urgently = data.get("is_urgently", False)

    print(f"[MAIN] Got AI response for mail {mail_id}")

    db_client.save_answer(mail_id, answer_text, is_important, is_urgently)

def start_consumer():
    mq.consume_ai_responses(ai_response_callback)


Thread(target=start_consumer, daemon=True).start()
