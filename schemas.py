from pydantic import BaseModel

class FlashcardCreate(BaseModel):
    student_id: str
    question: str
    answer: str

class FlashcardOut(BaseModel):
    question: str
    answer: str
    subject: str
