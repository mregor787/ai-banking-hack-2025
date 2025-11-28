from pydantic import BaseModel
from models import PersonType
from uuid import UUID


class MailCreate(BaseModel):
    mailText: str

class AnswerCreate(BaseModel):
    answerText: str
    isImportant: bool = False
    isUrgently: bool = False

class CustomerCreate(BaseModel):
    name: str
    personType: PersonType

class Customer(BaseModel):
    uuid: UUID
    name: str
    personType: PersonType

    class Config:
        orm_mode = True