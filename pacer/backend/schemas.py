from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class VectorAxis(BaseModel):
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

class VectorHistoryEntry(VectorAxis):
    vector_id: str
    assessment_id: str
    student_id: str
    created_at: datetime

class AssessmentCreate(BaseModel):
    student_id: str
    assessment_type: str
    source_ref_id: Optional[str] = None
    notes: Optional[str] = None
    vector_data: VectorAxis

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
    status: str
    ai_summary: str
    vector_start_id: str
    vector_end_id: str
    coach_comment: Optional[str] = None

class LLMFeedback(BaseModel):
    log_id: int
    coach_feedback: str
    reason_code: Optional[str] = None
