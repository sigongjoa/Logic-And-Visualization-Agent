from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
    Table,
    CheckConstraint,
    Float, # Added Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

# Association Tables
student_coach_relation = Table(
    "student_coach_relation",
    Base.metadata,
    Column("student_id", String(50), ForeignKey("students.student_id"), primary_key=True),
    Column("coach_id", String(50), ForeignKey("coaches.coach_id"), primary_key=True),
)

student_parent_association = Table(
    "student_parent_association",
    Base.metadata,
    Column("student_id", String(50), ForeignKey("students.student_id"), primary_key=True),
    Column("parent_id", Integer, ForeignKey("parents.parent_id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"
    student_id = Column(String(50), primary_key=True)
    student_name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    coaches = relationship("Coach", secondary=student_coach_relation, back_populates="students")
    parents = relationship("Parent", secondary=student_parent_association, back_populates="students")


class Coach(Base):
    __tablename__ = "coaches"
    coach_id = Column(String(50), primary_key=True)
    coach_name = Column(String(100), nullable=False)

    students = relationship("Student", secondary=student_coach_relation, back_populates="coaches")


class Parent(Base):
    __tablename__ = "parents"
    parent_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_name = Column(String(100), nullable=False)
    kakao_user_id = Column(String(255), unique=True, nullable=True)

    students = relationship("Student", secondary=student_parent_association, back_populates="parents")


class Assessment(Base):
    __tablename__ = "assessments"
    assessment_id = Column(String(50), primary_key=True)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    assessment_date = Column(DateTime(timezone=True), server_default=func.now())
    assessment_type = Column(String(20), nullable=False)
    source_ref_id = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    ai_model_version = Column(String(50), nullable=True)
    ai_reason_code = Column(String(50), nullable=True)


class StudentVectorHistory(Base):
    __tablename__ = "student_vector_history"
    vector_id = Column(String(50), primary_key=True)
    assessment_id = Column(String(50), ForeignKey("assessments.assessment_id"), nullable=False)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    axis1_geo = Column(Integer, CheckConstraint("axis1_geo BETWEEN 0 AND 100"), nullable=False)
    axis1_alg = Column(Integer, CheckConstraint("axis1_alg BETWEEN 0 AND 100"), nullable=False)
    axis1_ana = Column(Integer, CheckConstraint("axis1_ana BETWEEN 0 AND 100"), nullable=False)
    axis2_opt = Column(Integer, CheckConstraint("axis2_opt BETWEEN 0 AND 100"), nullable=False)
    axis2_piv = Column(Integer, CheckConstraint("axis2_piv BETWEEN 0 AND 100"), nullable=False)
    axis2_dia = Column(Integer, CheckConstraint("axis2_dia BETWEEN 0 AND 100"), nullable=False)
    axis3_con = Column(Integer, CheckConstraint("axis3_con BETWEEN 0 AND 100"), nullable=False)
    axis3_pro = Column(Integer, CheckConstraint("axis3_pro BETWEEN 0 AND 100"), nullable=False)
    axis3_ret = Column(Integer, CheckConstraint("axis3_ret BETWEEN 0 AND 100"), nullable=False)
    axis4_acc = Column(Integer, CheckConstraint("axis4_acc BETWEEN 0 AND 100"), nullable=False)
    axis4_gri = Column(Integer, CheckConstraint("axis4_gri BETWEEN 0 AND 100"), nullable=False)


class Curriculum(Base):
    __tablename__ = "curriculums"
    curriculum_id = Column(String(50), primary_key=True)
    curriculum_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)


class ConceptsLibrary(Base):
    __tablename__ = "concepts_library"
    concept_id = Column(String(50), primary_key=True)
    curriculum_id = Column(String(50), ForeignKey("curriculums.curriculum_id"))
    concept_name = Column(String(100), nullable=False)
    manim_data_path = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)


class ConceptRelation(Base):
    __tablename__ = "concept_relations"
    relation_id = Column(Integer, primary_key=True, autoincrement=True)
    from_concept_id = Column(String(50), ForeignKey("concepts_library.concept_id"))
    to_concept_id = Column(String(50), ForeignKey("concepts_library.concept_id"))
    relation_type = Column(String(20))


class StudentMastery(Base):
    __tablename__ = "student_mastery"
    student_id = Column(String(50), ForeignKey("students.student_id"), primary_key=True)
    concept_id = Column(String(50), ForeignKey("concepts_library.concept_id"), primary_key=True)
    mastery_score = Column(Integer, CheckConstraint("mastery_score BETWEEN 0 AND 100"), nullable=False)
    status = Column(String(20))
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())




class Submission(Base):
    __tablename__ = "submissions"
    submission_id = Column(String(50), primary_key=True)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    problem_text = Column(Text)
    status = Column(String(20), nullable=False)
    logical_path_text = Column(Text, nullable=True)
    concept_id = Column(String(50), ForeignKey("concepts_library.concept_id"), nullable=True)
    manim_data_path = Column(String(255), nullable=True)
    audio_explanation_url = Column(String(255), nullable=True) # New field for audio explanation URL
    manim_visualization_json = Column(Text, nullable=True)
    student_answer = Column(Text, nullable=True)


class CoachMemo(Base):
    __tablename__ = "coach_memos"
    memo_id = Column(Integer, primary_key=True, autoincrement=True)
    coach_id = Column(String(50), ForeignKey("coaches.coach_id"), nullable=False)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    memo_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LLMLog(Base):
    __tablename__ = "llm_logs"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    source_submission_id = Column(String(50), ForeignKey("submissions.submission_id"), nullable=True)
    coach_id = Column(String(50), ForeignKey("coaches.coach_id"), nullable=True)
    decision = Column(String(50), nullable=False)
    model_version = Column(String(50))
    coach_feedback = Column(Text, nullable=True)
    reason_code = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnkiCard(Base):
    __tablename__ = "anki_cards"
    card_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    llm_log_id = Column(Integer, ForeignKey("llm_logs.log_id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    next_review_date = Column(DateTime, nullable=False)
    # SM2 algorithm fields
    interval_days = Column(Integer, default=0)
    ease_factor = Column(Float, default=2.5)
    repetitions = Column(Integer, default=0)


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(50), ForeignKey("students.student_id"), nullable=False)
    coach_id = Column(String(50), ForeignKey("coaches.coach_id"), nullable=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="DRAFT")
    ai_summary = Column(Text, nullable=True)
    vector_start_id = Column(String(50), ForeignKey("student_vector_history.vector_id"))
    vector_end_id = Column(String(50), ForeignKey("student_vector_history.vector_id"))
    coach_comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finalized_at = Column(DateTime(timezone=True), nullable=True)
