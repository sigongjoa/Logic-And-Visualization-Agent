from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class VectorHistoryEntry(BaseModel):
    vector_id: str
    assessment_id: str
    student_id: str
    created_at: datetime
    axis1_geo: int = Field(..., ge=0, le=100)
    axis1_alg: int = Field(..., ge=0, le=100)
    axis1_ana: int = Field(..., ge=0, le=100)
    axis2_opt: int = Field(..., ge=0, le=100)
    axis2_piv: int = Field(..., ge=0, le=100)
    axis2_dia: int = Field(..., ge=0, le=100)
    axis3_con: int = Field(..., ge=0, le=100)
    axis3_pro: int = Field(..., ge=0, le=100)
    axis3_ret: int = Field(..., ge=0, le=100)
    axis4_acc: int = Field(..., ge=0, le=100)
    axis4_gri: int = Field(..., ge=0, le=100)

class AssessmentCreate(BaseModel):
    student_id: str
    assessment_type: str
    source_ref_id: Optional[str] = None
    notes: Optional[str] = None
    vector_data: dict = Field(
        ...,
        example={
            "axis1_geo": 70, "axis1_alg": 60, "axis1_ana": 75,
            "axis2_opt": 80, "axis2_piv": 65, "axis2_dia": 70,
            "axis3_con": 85, "axis3_pro": 70, "axis3_ret": 75,
            "axis4_acc": 90, "axis4_gri": 80
        }
    )

class SubmissionCreate(BaseModel):
    student_id: str
    problem_text: str

class SubmissionResult(BaseModel):
    submission_id: str
    status: str
    logical_path_text: str
    concept_id: str
    manim_content_url: str

class CoachMemoCreate(BaseModel):
    coach_id: str
    student_id: str
    memo_text: str

class WeeklyReport(BaseModel):
    report_id: int
    student_id: str
    coach_id: Optional[str] = None
    period_start: datetime
    period_end: datetime
    status: str
    ai_summary: str
    vector_start_id: str
    vector_end_id: str
    coach_comment: Optional[str] = None
    created_at: datetime
    finalized_at: Optional[datetime] = None

class LLMFeedback(BaseModel):
    log_id: int
    coach_feedback: str
    reason_code: Optional[str] = None

class CoachComment(BaseModel):
    coach_comment: str


class Curriculum(BaseModel):
    curriculum_id: str
    curriculum_name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class Concept(BaseModel):
    concept_id: str
    curriculum_id: Optional[str] = None
    concept_name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ConceptRelation(BaseModel):
    relation_id: int
    from_concept_id: str
    to_concept_id: str
    relation_type: str
    model_config = ConfigDict(from_attributes=True)


class StudentMastery(BaseModel):
    student_id: str
    concept_id: str
    mastery_score: int
    status: Optional[str] = None
    last_updated: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)