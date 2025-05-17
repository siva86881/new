from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Flashcard
from schemas import FlashcardCreate, FlashcardOut
from classifier import infer_subject
import random

from models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/flashcard")
def add_flashcard(flashcard: FlashcardCreate, db: Session = Depends(get_db)):
    subject = infer_subject(flashcard.question)
    db_card = Flashcard(**flashcard.dict(), subject=subject)
    db.add(db_card)
    db.commit()
    return {"message": "Flashcard added successfully", "subject": subject}

@app.get("/get-subject", response_model=list[FlashcardOut])
def get_mixed_flashcards(student_id: str, limit: int = 5, db: Session = Depends(get_db)):
    all_cards = db.query(Flashcard).filter(Flashcard.student_id == student_id).all()
    subject_groups = {}
    for card in all_cards:
        subject_groups.setdefault(card.subject, []).append(card)

    mixed_cards = []
    while len(mixed_cards) < limit and subject_groups:
        for subject in list(subject_groups):
            if subject_groups[subject]:
                mixed_cards.append(subject_groups[subject].pop())
                if len(mixed_cards) == limit:
                    break
            if not subject_groups[subject]:
                del subject_groups[subject]

    random.shuffle(mixed_cards)
    return mixed_cards
