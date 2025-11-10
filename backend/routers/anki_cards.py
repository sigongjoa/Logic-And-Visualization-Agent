from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, crud
from backend.main import get_db
from typing import Optional

import logging # Added import

router = APIRouter(
    prefix="/anki-cards",
    tags=["Anki Cards"],
)

logger = logging.getLogger(__name__) # Added logger

@router.patch("/{card_id}/review", response_model=schemas.AnkiCard)
def review_anki_card(
    card_id: int, review: schemas.AnkiCardReview, db: Session = Depends(get_db)
):
    logger.debug(f"API: Received review for card_id={card_id} with grade={review.grade}")
    
    db_anki_card = crud.update_anki_card_sm2(db=db, card_id=card_id, grade=review.grade)
    if db_anki_card is None:
        logger.warning(f"API: Anki Card with ID {card_id} not found for review.")
        raise HTTPException(status_code=404, detail="Anki Card not found.")
    
    logger.debug(f"API: Successfully reviewed card_id={card_id}. New next_review_date={db_anki_card.next_review_date}")
    return db_anki_card

@router.get("/student/{student_id}", response_model=list[schemas.AnkiCard])
def get_anki_cards_for_student(student_id: str, db: Session = Depends(get_db)):
    anki_cards = crud.get_anki_cards_by_student(db, student_id)
    return anki_cards
