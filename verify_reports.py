from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, WeeklyReport, Student
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./atlas.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_weekly_reports():
    db = next(get_db())
    try:
        print("Verifying Weekly Reports:")
        reports = db.query(WeeklyReport).all()
        if not reports:
            print("No weekly reports found.")
            return

        for report in reports:
            student = db.query(Student).filter(Student.student_id == report.student_id).first()
            student_name = student.student_name if student else "Unknown Student"
            print(f"--- Report ID: {report.report_id} ---")
            print(f"  Student: {student_name} ({report.student_id})")
            print(f"  Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}")
            print(f"  Status: {report.status}")
            print(f"  AI Summary:\n{report.ai_summary}")
            print(f"  Coach Comment: {report.coach_comment}")
            print("-" * 30)

    except Exception as e:
        print(f"Error verifying weekly reports: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_weekly_reports()
