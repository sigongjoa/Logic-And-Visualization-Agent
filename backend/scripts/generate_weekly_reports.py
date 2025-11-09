import asyncio
from sqlalchemy.orm import Session
from backend import models, crud, schemas
from backend.main import SessionLocal, engine
from datetime import datetime, timedelta

async def generate_weekly_reports(db: Session):
    with open("report_generation.log", "a") as log_file:
        try:
            # 1. Get all students
            students = db.query(models.Student).all()
            log_file.write(f"Found {len(students)} students.\n")

            for student in students:
                log_file.write(f"Processing student: {student.student_name}\n")
                # 2. Get vectors for the student
                today = datetime.utcnow()
                one_week_ago = today - timedelta(days=7)

                latest_vector = crud.get_latest_vector_for_student(db, student.student_id)
                
                weekly_start_vector = db.query(models.StudentVectorHistory).filter(
                    models.StudentVectorHistory.student_id == student.student_id,
                    models.StudentVectorHistory.created_at >= one_week_ago
                ).order_by(models.StudentVectorHistory.created_at.asc()).first()

                log_file.write(f"Latest vector: {latest_vector}\n")
                log_file.write(f"Weekly start vector: {weekly_start_vector}\n")

                if not latest_vector or not weekly_start_vector:
                    log_file.write(f"Not enough data to generate a report for {student.student_name}\n")
                    continue

                # 3. Generate a more detailed AI summary
                summary = f"Weekly Report for {student.student_name} (Period: {one_week_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')})\n\n"

                # Vector Analysis
                summary += "--- 4-Axis Model Progress ---\n"
                summary += f"Start of week (Accuracy/Grit): {weekly_start_vector.axis4_acc}/{weekly_start_vector.axis4_gri}\n"
                summary += f"End of week (Accuracy/Grit): {latest_vector.axis4_acc}/{latest_vector.axis4_gri}\n"
                
                change_acc = latest_vector.axis4_acc - weekly_start_vector.axis4_acc
                change_gri = latest_vector.axis4_gri - weekly_start_vector.axis4_gri
                summary += f"Weekly change in Accuracy: {'+' if change_acc > 0 else ''}{change_acc}\n"
                summary += f"Weekly change in Grit: {'+' if change_gri > 0 else ''}{change_gri}\n\n"

                # Submissions Analysis
                submissions_in_period = db.query(models.Submission).filter(
                    models.Submission.student_id == student.student_id,
                    models.Submission.submitted_at >= one_week_ago,
                    models.Submission.submitted_at <= today
                ).all()
                
                if submissions_in_period:
                    summary += "--- Submissions This Week ---\n"
                    for sub in submissions_in_period:
                        summary += f"- Problem: '{sub.problem_text}' (Concept: {sub.concept_id or 'N/A'})\n"
                        logical_path_snippet = (sub.logical_path_text[:50] + "...") if sub.logical_path_text else "N/A"
                        summary += f"  Status: {sub.status}, Logical Path: {logical_path_snippet}\n"
                    summary += "\n"
                else:
                    summary += "--- No Submissions This Week ---\n\n"

                # Mastery Changes Analysis
                mastery_changes_in_period = db.query(models.StudentMastery).filter(
                    models.StudentMastery.student_id == student.student_id,
                    models.StudentMastery.last_updated >= one_week_ago,
                    models.StudentMastery.last_updated <= today
                ).all()

                if mastery_changes_in_period:
                    summary += "--- Mastery Updates This Week ---\n"
                    for mc in mastery_changes_in_period:
                        summary += f"- Concept: {mc.concept_id}, Score: {mc.mastery_score}, Status: {mc.status}\n"
                    summary += "\n"
                else:
                    summary += "--- No Mastery Updates This Week ---\n\n"

                log_file.write(f"Generated summary: {summary}\n")

                # 4. Create the DRAFT report
                report = models.WeeklyReport(
                    student_id=student.student_id,
                    period_start=one_week_ago,
                    period_end=today,
                    status="DRAFT",
                    ai_summary=summary,
                    vector_start_id=weekly_start_vector.vector_id,
                    vector_end_id=latest_vector.vector_id,
                )
                db.add(report)
                db.commit()
                log_file.write(f"Generated DRAFT report for {student.student_name}\n")

        finally:
            db.close()

if __name__ == "__main__":
    # This script is intended to be run as a scheduled job.
    # For V1, we run it manually.
    models.Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    asyncio.run(generate_weekly_reports(db=db_session))
