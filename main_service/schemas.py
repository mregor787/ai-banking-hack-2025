from pydantic import BaseModel
from enum import Enum


class PersonType(str, Enum):
    individual = "individual"
    corporate = "corporate"
    government = "government"


class MailIn(BaseModel):
    customerId: str
    mailText: str


class CustomerIn(BaseModel):
    name: str
    personType: PersonType