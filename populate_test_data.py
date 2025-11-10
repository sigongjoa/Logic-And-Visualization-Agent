from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models, schemas, crud
from datetime import datetime, timedelta, timezone
import uuid
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

def populate_test_data():
    db = next(get_db())
    try:
        # Ensure tables are created
        models.Base.metadata.create_all(bind=engine)

        # Clear existing test data to avoid conflicts
        db.query(models.StudentVectorHistory).delete()
        db.query(models.Assessment).delete()
        db.query(models.Submission).delete()
        db.query(models.StudentMastery).delete()
        db.query(models.Student).delete()
        db.commit()

        # 1. Create a dummy student
        student_id = "std_test_report"
        student_name = "Test Report Student"
        student_schema = schemas.StudentCreate(student_id=student_id, student_name=student_name)
        crud.create_student(db, student_schema)
        print(f"Created student: {student_name}")

        # Ensure a concept exists for mastery
        concept_id = "C_MATH_TEST"
        if not db.query(models.ConceptsLibrary).filter_by(concept_id=concept_id).first():
            # Assuming M-ALL curriculum exists from populate_knowledge_graph
            if not db.query(models.Curriculum).filter_by(curriculum_id="M-ALL").first():
                db.add(models.Curriculum(curriculum_id="M-ALL", curriculum_name="중등 수학: 공통 기초"))
                db.commit()
            db.add(models.ConceptsLibrary(concept_id=concept_id, curriculum_id="M-ALL", concept_name="테스트 개념"))
            db.commit()
        print(f"Ensured concept: {concept_id}")

        # 2. Create two StudentVectorHistory entries for the student
        today = datetime.now(timezone.utc)
        one_week_ago = today - timedelta(days=7)

        # Vector for one week ago
        assessment_id_1 = f"asmt_{uuid.uuid4().hex[:8]}"
        vector_data_1 = {
            "axis1_geo": 50, "axis1_alg": 50, "axis1_ana": 50,
            "axis2_opt": 50, "axis2_piv": 50, "axis2_dia": 50,
            "axis3_con": 50, "axis3_pro": 50, "axis3_ret": 50,
            "axis4_acc": 50, "axis4_gri": 50,
        }
        assessment_schema_1 = schemas.AssessmentCreate(
            student_id=student_id,
            assessment_type="MANUAL",
            source_ref_id=None,
            notes="Initial vector for report test",
            vector_data=vector_data_1
        )
        db_assessment_1 = models.Assessment(
            assessment_id=assessment_id_1,
            student_id=student_id,
            assessment_date=one_week_ago - timedelta(hours=1), # Ensure it's before one_week_ago
            assessment_type="MANUAL",
            source_ref_id=None,
            notes="Initial vector for report test"
        )
        db.add(db_assessment_1)
        db.flush()
        db_vector_1 = models.StudentVectorHistory(
            vector_id=f"vec_{uuid.uuid4().hex[:8]}",
            assessment_id=assessment_id_1,
            student_id=student_id,
            created_at=one_week_ago - timedelta(hours=1),
            **vector_data_1
        )
        db.add(db_vector_1)
        db.commit()
        print(f"Created initial vector history for {student_name}")

        # Vector for today (showing some change)
        assessment_id_2 = f"asmt_{uuid.uuid4().hex[:8]}"
        vector_data_2 = {
            "axis1_geo": 55, "axis1_alg": 55, "axis1_ana": 55,
            "axis2_opt": 55, "axis2_piv": 55, "axis2_dia": 55,
            "axis3_con": 55, "axis3_pro": 55, "axis3_ret": 55,
            "axis4_acc": 60, "axis4_gri": 60, # Changed for report
        }
        assessment_schema_2 = schemas.AssessmentCreate(
            student_id=student_id,
            assessment_type="MANUAL",
            source_ref_id=None,
            notes="Latest vector for report test",
            vector_data=vector_data_2
        )
        db_assessment_2 = models.Assessment(
            assessment_id=assessment_id_2,
            student_id=student_id,
            assessment_date=today - timedelta(hours=1), # Ensure it's before today
            assessment_type="MANUAL",
            source_ref_id=None,
            notes="Latest vector for report test"
        )
        db.add(db_assessment_2)
        db.flush()
        db_vector_2 = models.StudentVectorHistory(
            vector_id=f"vec_{uuid.uuid4().hex[:8]}",
            assessment_id=assessment_id_2,
            student_id=student_id,
            created_at=today - timedelta(hours=1),
            **vector_data_2
        )
        db.add(db_vector_2)
        db.commit()
        print(f"Created latest vector history for {student_name}")

        # 3. Create some dummy submissions
        submission_id_1 = f"sub_{uuid.uuid4().hex[:8]}"
        db.add(models.Submission(
            submission_id=submission_id_1,
            student_id=student_id,
            submitted_at=one_week_ago + timedelta(days=1),
            problem_text="Report Problem 1",
            status="COMPLETE",
            logical_path_text="Logical path for problem 1",
            concept_id=concept_id
        ))
        submission_id_2 = f"sub_{uuid.uuid4().hex[:8]}"
        db.add(models.Submission(
            submission_id=submission_id_2,
            student_id=student_id,
            submitted_at=today - timedelta(days=1),
            problem_text="Report Problem 2",
            status="PENDING",
            logical_path_text="Logical path for problem 2",
            concept_id=concept_id
        ))
        db.commit()
        print(f"Created dummy submissions for {student_name}")

        # 4. Create a StudentMastery entry
        db.add(models.StudentMastery(
            student_id=student_id,
            concept_id=concept_id,
            mastery_score=70,
            status="IN_PROGRESS",
            last_updated=today - timedelta(days=2)
        ))
        db.commit()
        print(f"Created dummy student mastery for {student_name}")

        print("Test data populated successfully!")

    except Exception as e:
        print(f"Error populating test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_test_data()
