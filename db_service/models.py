from sqlalchemy import Column, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
import enum
from datetime import datetime

Base = declarative_base()

class PersonType(str, enum.Enum):
    individual = "individual"
    corporate = "corporate"
    government = "government"

class Customer(Base):
    __tablename__ = "customers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    personType = Column(Enum(PersonType), nullable=False)

    mails = relationship("Mail", back_populates="customer")

class Mail(Base):
    __tablename__ = "mails"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    mailText = Column(String, nullable=False)

    customerId_ref = Column(UUID(as_uuid=True), ForeignKey("customers.uuid"))
    customer = relationship("Customer", back_populates="mails")

    answer = relationship("Answer", back_populates="mail", uselist=False)

class Answer(Base):
    __tablename__ = "answers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    answerText = Column(String, nullable=False)

    isImportant = Column(Boolean, default=False)
    isUrgently = Column(Boolean, default=False)

    mailId_ref = Column(UUID(as_uuid=True), ForeignKey("mails.uuid"))
    mail = relationship("Mail", back_populates="answer")
