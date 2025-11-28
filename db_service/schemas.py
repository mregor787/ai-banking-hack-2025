from pydantic import BaseModel


class MailCreate(BaseModel):
    mailText: str

class AnswerCreate(BaseModel):
    answerText: str
    isImportant: bool = False
    isUrgently: bool = False
