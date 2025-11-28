from sqlalchemy.orm import Session
from models import Mail, Answer, Customer
from schemas import MailCreate, AnswerCreate, CustomerCreate


def get_all_mails(db: Session):
    return db.query(Mail).all()

def get_mail(db: Session, mail_id):
    return db.query(Mail).filter(Mail.uuid == mail_id).first()

def create_mail(db: Session, customer_id, mail_data: MailCreate):
    mail = Mail(
        mailText=mail_data.mailText,
        customerId_ref=customer_id
    )
    db.add(mail)
    db.commit()
    db.refresh(mail)
    return mail

def create_answer(db: Session, mail_id, answer_data: AnswerCreate):
    answer = Answer(
        mailId_ref=mail_id,
        answerText=answer_data.answerText,
        isImportant=answer_data.isImportant,
        isUrgently=answer_data.isUrgently
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer

def get_customers(db: Session):
    return db.query(Customer).all()

def create_customer(db: Session, customer_data: CustomerCreate):
    customer = Customer(
        name=customer_data.name,
        personType=customer_data.personType
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer
