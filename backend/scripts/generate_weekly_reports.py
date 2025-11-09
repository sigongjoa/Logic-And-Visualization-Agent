import asyncio
from sqlalchemy.orm import Session
from backend import models, crud, schemas
from backend.main import SessionLocal, engine
from datetime import datetime, timedelta, timezone # Added timezone

async def generate_weekly_reports(db: Session):
    with open("report_generation.log", "a") as log_file:
        try:
            # 1. Get all students
            students = db.query(models.Student).all()
            log_file.write(f"Found {len(students)} students.\n")

            for student in students:
                log_file.write(f"Processing student: {student.student_name}\n")
                # 2. Get vectors for the student
                today = datetime.now(timezone.utc)
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
                summary = f"주간 학습 리포트 - {student.student_name} (기간: {one_week_ago.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')})\n\n"

                # Vector Analysis
                summary += "--- 4축 모델 변화 ---\n"
                change_acc = latest_vector.axis4_acc - weekly_start_vector.axis4_acc
                change_gri = latest_vector.axis4_gri - weekly_start_vector.axis4_gri

                acc_status = "향상되었습니다." if change_acc > 0 else ("유지되었습니다." if change_acc == 0 else "조금 감소했습니다.")
                gri_status = "향상되었습니다." if change_gri > 0 else ("유지되었습니다." if change_gri == 0 else "조금 감소했습니다.")

                summary += f"이번 주 연산 정확성(axis4_acc)은 {latest_vector.axis4_acc}점으로, 지난 주 대비 {abs(change_acc)}점 {acc_status}\n"
                summary += f"난이도 내성(axis4_gri)은 {latest_vector.axis4_gri}점으로, 지난 주 대비 {abs(change_gri)}점 {gri_status}\n\n"

                # Submissions Analysis
                submissions_in_period = db.query(models.Submission).filter(
                    models.Submission.student_id == student.student_id,
                    models.Submission.submitted_at >= one_week_ago,
                    models.Submission.submitted_at <= today
                ).all()
                
                if submissions_in_period:
                    summary += "--- 이번 주 학습 활동 ---\n"
                    completed_submissions = [s for s in submissions_in_period if s.status == "COMPLETE"]
                    pending_submissions = [s for s in submissions_in_period if s.status == "PENDING"]
                    
                    summary += f"총 {len(submissions_in_period)}개의 문제를 제출했습니다. 그 중 {len(completed_submissions)}개를 완료했습니다.\n"
                    if pending_submissions:
                        summary += f"미완료 문제: {', '.join([s.problem_text for s in pending_submissions[:2]])}{'...' if len(pending_submissions) > 2 else ''}\n"
                    summary += "\n"
                else:
                    summary += "--- 이번 주 제출된 학습 활동이 없습니다. ---\n\n"

                # Mastery Changes Analysis
                mastery_changes_in_period = db.query(models.StudentMastery).filter(
                    models.StudentMastery.student_id == student.student_id,
                    models.StudentMastery.last_updated >= one_week_ago,
                    models.StudentMastery.last_updated <= today
                ).all()

                if mastery_changes_in_period:
                    summary += "--- 개념 숙련도 변화 ---\n"
                    mastered_concepts = [mc for mc in mastery_changes_in_period if mc.status == "MASTERED"]
                    improved_concepts = [mc for mc in mastery_changes_in_period if mc.status == "IN_PROGRESS" and mc.mastery_score > 50] # Simple heuristic for improvement
                    
                    if mastered_concepts:
                        summary += f"새롭게 숙달한 개념: {', '.join([mc.concept_id for mc in mastered_concepts])}\n"
                    if improved_concepts:
                        summary += f"숙련도가 향상된 개념: {', '.join([mc.concept_id for mc in improved_concepts])}\n"
                    summary += "\n"
                else:
                    summary += "--- 이번 주 개념 숙련도 변화가 없습니다. ---\n\n"

                # Overall Concluding Remark
                if change_acc > 0 and change_gri > 0:
                    summary += "전반적으로 연산 정확성과 난이도 내성 모두 긍정적인 변화를 보였습니다. 꾸준한 학습 태도가 돋보입니다.\n"
                elif change_acc > 0 or change_gri > 0:
                    summary += "일부 영역에서 긍정적인 변화가 있었으나, 다른 영역에서는 추가적인 관심이 필요해 보입니다.\n"
                else:
                    summary += "이번 주에는 큰 변화가 없었지만, 꾸준히 학습에 참여하고 있습니다. 다음 주에는 더 큰 발전을 기대합니다.\n"
                
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
