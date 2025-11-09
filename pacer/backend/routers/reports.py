from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pacer.backend import schemas, crud
from pacer.backend.main import get_db

router = APIRouter(
    prefix="/reports",
    tags=["Reporting"],
)

@router.get("/drafts", response_model=List[schemas.WeeklyReport])
def get_report_drafts(db: Session = Depends(get_db)):
    drafts = crud.get_report_drafts(db=db)
    return drafts

@router.put("/{report_id}/finalize", response_model=schemas.WeeklyReport)
def finalize_report(
    report_id: int,
    report_data: schemas.CoachComment,
    db: Session = Depends(get_db)
):
    db_report = crud.get_report(db=db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if db_report.status != "DRAFT":
        raise HTTPException(status_code=400, detail="Report is not a draft")

    return crud.finalize_report(db=db, report_id=report_id, comment=report_data.coach_comment)

@router.post("/{report_id}/send")
def send_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report(db=db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if db_report.status != "FINALIZED":
        raise HTTPException(status_code=400, detail="Report is not finalized")

    crud.send_report(db=db, report_id=report_id)
    return {"message": "Report sent successfully"}
