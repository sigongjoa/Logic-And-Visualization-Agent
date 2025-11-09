import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Add the parent directory to the path to allow imports from 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend import models

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./atlas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Data from ATLAS_Curriculum_Knowledge_Graph_Specification.md
curriculums = [
    {"curriculum_id": "M-ALL", "curriculum_name": "중등 수학: 공통 기초"},
    {"curriculum_id": "H-COMMON", "curriculum_name": "고등 수학 (상), (하)"},
    {"curriculum_id": "MATH-I", "curriculum_name": "수학 I"},
    {"curriculum_id": "MATH-II", "curriculum_name": "수학 II"},
    {"curriculum_id": "CALC", "curriculum_name": "미적분 - 선택"},
    {"curriculum_id": "PSTAT", "curriculum_name": "확률과 통계 - 선택"},
    {"curriculum_id": "GEO", "curriculum_name": "기하 - 선택"},
]

concepts = [
    # M-ALL
    {"concept_id": "C-M-001", "curriculum_id": "M-ALL", "concept_name": "소인수분해"},
    {"concept_id": "C-M-002", "curriculum_id": "M-ALL", "concept_name": "정수와 유리수"},
    {"concept_id": "C-M-003", "curriculum_id": "M-ALL", "concept_name": "일차방정식의 풀이"},
    {"concept_id": "C-M-004", "curriculum_id": "M-ALL", "concept_name": "다항식의 연산"},
    {"concept_id": "C-M-005", "curriculum_id": "M-ALL", "concept_name": "곱셈 공식 및 인수분해"},
    {"concept_id": "C-M-006", "curriculum_id": "M-ALL", "concept_name": "일차함수와 그래프"},
    {"concept_id": "C-M-007", "curriculum_id": "M-ALL", "concept_name": "이차함수와 그래프"},
    {"concept_id": "C-M-008", "curriculum_id": "M-ALL", "concept_name": "도형의 닮음"},
    {"concept_id": "C-M-009", "curriculum_id": "M-ALL", "concept_name": "피타고라스의 정리"},
    {"concept_id": "C-M-010", "curriculum_id": "M-ALL", "concept_name": "삼각비"},
    {"concept_id": "C-M-011", "curriculum_id": "M-ALL", "concept_name": "경우의 수"},

    # H-COMMON
    {"concept_id": "C-H-001", "curriculum_id": "H-COMMON", "concept_name": "항등식과 나머지 정리"},
    {"concept_id": "C-H-002", "curriculum_id": "H-COMMON", "concept_name": "인수분해 (고차식)"},
    {"concept_id": "C-H-003", "curriculum_id": "H-COMMON", "concept_name": "복소수"},
    {"concept_id": "C-H-004", "curriculum_id": "H-COMMON", "concept_name": "이차방정식"},
    {"concept_id": "C-H-005", "curriculum_id": "H-COMMON", "concept_name": "이차함수와 이차방정식의 관계"},
    {"concept_id": "C-H-006", "curriculum_id": "H-COMMON", "concept_name": "원의 방정식"},
    {"concept_id": "C-H-007", "curriculum_id": "H-COMMON", "concept_name": "합성함수와 역함수"},
    {"concept_id": "C-H-008", "curriculum_id": "H-COMMON", "concept_name": "순열"},
    {"concept_id": "C-H-009", "curriculum_id": "H-COMMON", "concept_name": "조합"},

    # MATH-I
    {"concept_id": "C-MI-001", "curriculum_id": "MATH-I", "concept_name": "지수/로그의 정의와 성질"},
    {"concept_id": "C-MI-002", "curriculum_id": "MATH-I", "concept_name": "지수/로그 함수와 그래프"},
    {"concept_id": "C-MI-003", "curriculum_id": "MATH-I", "concept_name": "삼각함수 그래프"},
    {"concept_id": "C-MI-004", "curriculum_id": "MATH-I", "concept_name": "사인법칙과 코사인법칙"},
    {"concept_id": "C-MI-005", "curriculum_id": "MATH-I", "concept_name": "시그마의 정의와 성질"},

    # MATH-II
    {"concept_id": "C-MII-001", "curriculum_id": "MATH-II", "concept_name": "함수의 극한"},
    {"concept_id": "C-MII-002", "curriculum_id": "MATH-II", "concept_name": "미분계수"},
    {"concept_id": "C-MII-003", "curriculum_id": "MATH-II", "concept_name": "도함수"},
    {"concept_id": "C-MII-004", "curriculum_id": "MATH-II", "concept_name": "부정적분"},
    {"concept_id": "C-MII-005", "curriculum_id": "MATH-II", "concept_name": "정적분"},
]

def populate():
    for curr in curriculums:
        if not db.query(models.Curriculum).filter_by(curriculum_id=curr["curriculum_id"]).first():
            db.add(models.Curriculum(**curr))

    for conc in concepts:
        if not db.query(models.ConceptsLibrary).filter_by(concept_id=conc["concept_id"]).first():
            db.add(models.ConceptsLibrary(**conc))
    
    db.commit()
    print("Database populated with curriculums and concepts.")

if __name__ == "__main__":
    populate()
