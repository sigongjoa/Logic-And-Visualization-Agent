from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, UTC
from typing import Optional
from . import kakao_sender # Import the kakao_sender

# ... (other functions)

def send_report(db: Session, report_id: int):
    db_report = get_report(db=db, report_id=report_id)
    if db_report:
        # Get student and parent information
        student = db.query(models.Student).filter(models.Student.student_id == db_report.student_id).first()
        if not student:
            print(f"Student with ID {db_report.student_id} not found for report {report_id}")
            return None

        parent_association = db.query(models.student_parent_association).filter(
            models.student_parent_association.c.student_id == student.student_id
        ).first()
        if not parent_association:
            print(f"No parent associated with student {student.student_id} for report {report_id}")
            return None
        
        parent = db.query(models.Parent).filter(models.Parent.parent_id == parent_association.parent_id).first()
        if not parent or not parent.kakao_user_id:
            print(f"Parent or Kakao user ID not found for student {student.student_id} for report {report_id}")
            return None

        # Construct the message
        message_title = f"주간 학습 리포트 - {student.student_name} ({db_report.period_start.strftime('%Y-%m-%d')} ~ {db_report.period_end.strftime('%Y-%m-%d')})"
        message_body = f"AI 요약:\n{db_report.ai_summary}\n\n코치 코멘트:\n{db_report.coach_comment or '코치 코멘트가 없습니다.'}"
        full_message = f"{message_title}\n\n{message_body}"

        # Simulate sending KakaoTalk message
        kakao_sender.send_kakao_message(parent.kakao_user_id, full_message)

        db_report.status = "SENT"
        db.commit()
        db.refresh(db_report)
    return db_report
