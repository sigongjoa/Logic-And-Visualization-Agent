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
    {"curriculum_id": "CALC", "curriculum_name": "미적분"},
    {"curriculum_id": "PSTAT", "curriculum_name": "확률과 통계"},
    {"curriculum_id": "GEO", "curriculum_name": "기하"},
]

concepts = [
    # M-ALL (중등 수학: 공통 기초)
    {"concept_id": "C-MALL-001", "curriculum_id": "M-ALL", "concept_name": "소인수분해"},
    {"concept_id": "C-MALL-002", "curriculum_id": "M-ALL", "concept_name": "정수와 유리수"},
    {"concept_id": "C-MALL-003", "curriculum_id": "M-ALL", "concept_name": "일차방정식의 풀이"},
    {"concept_id": "C-MALL-004", "curriculum_id": "M-ALL", "concept_name": "다항식의 연산"},
    {"concept_id": "C-MALL-005", "curriculum_id": "M-ALL", "concept_name": "곱셈 공식 및 인수분해"},
    {"concept_id": "C-MALL-006", "curriculum_id": "M-ALL", "concept_name": "좌표평면과 그래프"},
    {"concept_id": "C-MALL-007", "curriculum_id": "M-ALL", "concept_name": "정비례와 반비례"},
    {"concept_id": "C-MALL-008", "curriculum_id": "M-ALL", "concept_name": "일차함수와 그래프"},
    {"concept_id": "C-MALL-009", "curriculum_id": "M-ALL", "concept_name": "이차함수와 그래프"},
    {"concept_id": "C-MALL-010", "curriculum_id": "M-ALL", "concept_name": "기본 도형"},
    {"concept_id": "C-MALL-011", "curriculum_id": "M-ALL", "concept_name": "삼각형/사각형의 성질"},
    {"concept_id": "C-MALL-012", "curriculum_id": "M-ALL", "concept_name": "도형의 닮음"},
    {"concept_id": "C-MALL-013", "curriculum_id": "M-ALL", "concept_name": "피타고라스의 정리"},
    {"concept_id": "C-MALL-014", "curriculum_id": "M-ALL", "concept_name": "삼각비"},
    {"concept_id": "C-MALL-015", "curriculum_id": "M-ALL", "concept_name": "경우의 수"},
    {"concept_id": "C-MALL-016", "curriculum_id": "M-ALL", "concept_name": "확률의 기본 성질"},

    # H-COMMON (고등 수학 (상), (하))
    {"concept_id": "C-HCOM-001", "curriculum_id": "H-COMMON", "concept_name": "항등식과 나머지 정리"},
    {"concept_id": "C-HCOM-002", "curriculum_id": "H-COMMON", "concept_name": "인수분해 (고차식)"},
    {"concept_id": "C-HCOM-003", "curriculum_id": "H-COMMON", "concept_name": "복소수"},
    {"concept_id": "C-HCOM-004", "curriculum_id": "H-COMMON", "concept_name": "이차방정식"},
    {"concept_id": "C-HCOM-005", "curriculum_id": "H-COMMON", "concept_name": "이차함수와 이차방정식의 관계"},
    {"concept_id": "C-HCOM-006", "curriculum_id": "H-COMMON", "concept_name": "평면좌표"},
    {"concept_id": "C-HCOM-007", "curriculum_id": "H-COMMON", "concept_name": "직선의 방정식"},
    {"concept_id": "C-HCOM-008", "curriculum_id": "H-COMMON", "concept_name": "원의 방정식"},
    {"concept_id": "C-HCOM-009", "curriculum_id": "H-COMMON", "concept_name": "도형의 이동"},
    {"concept_id": "C-HCOM-010", "curriculum_id": "H-COMMON", "concept_name": "집합의 연산"},
    {"concept_id": "C-HCOM-011", "curriculum_id": "H-COMMON", "concept_name": "명제"},
    {"concept_id": "C-HCOM-012", "curriculum_id": "H-COMMON", "concept_name": "함수 (일대일, 항등, 상수)"},
    {"concept_id": "C-HCOM-013", "curriculum_id": "H-COMMON", "concept_name": "합성함수와 역함수"},
    {"concept_id": "C-HCOM-014", "curriculum_id": "H-COMMON", "concept_name": "유리함수와 무리함수"},
    {"concept_id": "C-HCOM-015", "curriculum_id": "H-COMMON", "concept_name": "순열"},
    {"concept_id": "C-HCOM-016", "curriculum_id": "H-COMMON", "concept_name": "조합"},

    # MATH-I (수학 I)
    {"concept_id": "C-MATH1-001", "curriculum_id": "MATH-I", "concept_name": "거듭제곱근"},
    {"concept_id": "C-MATH1-002", "curriculum_id": "MATH-I", "concept_name": "지수/로그의 정의와 성질"},
    {"concept_id": "C-MATH1-003", "curriculum_id": "MATH-I", "concept_name": "지수/로그 함수와 그래프"},
    {"concept_id": "C-MATH1-004", "curriculum_id": "MATH-I", "concept_name": "일반각과 호도법"},
    {"concept_id": "C-MATH1-005", "curriculum_id": "MATH-I", "concept_name": "삼각함수 그래프"},
    {"concept_id": "C-MATH1-006", "curriculum_id": "MATH-I", "concept_name": "사인법칙과 코사인법칙"},
    {"concept_id": "C-MATH1-007", "curriculum_id": "MATH-I", "concept_name": "등차/등비수열"},
    {"concept_id": "C-MATH1-008", "curriculum_id": "MATH-I", "concept_name": "시그마의 정의와 성질"},
    {"concept_id": "C-MATH1-009", "curriculum_id": "MATH-I", "concept_name": "수학적 귀납법"},

    # MATH-II (수학 II)
    {"concept_id": "C-MATH2-001", "curriculum_id": "MATH-II", "concept_name": "함수의 극한"},
    {"concept_id": "C-MATH2-002", "curriculum_id": "MATH-II", "concept_name": "함수의 연속성"},
    {"concept_id": "C-MATH2-003", "curriculum_id": "MATH-II", "concept_name": "미분계수"},
    {"concept_id": "C-MATH2-004", "curriculum_id": "MATH-II", "concept_name": "도함수"},
    {"concept_id": "C-MATH2-005", "curriculum_id": "MATH-II", "concept_name": "접선의 방정식"},
    {"concept_id": "C-MATH2-006", "curriculum_id": "MATH-II", "concept_name": "함수의 증가/감소, 극대/극소"},
    {"concept_id": "C-MATH2-007", "curriculum_id": "MATH-II", "concept_name": "부정적분"},
    {"concept_id": "C-MATH2-008", "curriculum_id": "MATH-II", "concept_name": "정적분"},
    {"concept_id": "C-MATH2-009", "curriculum_id": "MATH-II", "concept_name": "정적분의 활용 (넓이)"},

    # CALC (미적분)
    {"concept_id": "C-CALC-001", "curriculum_id": "CALC", "concept_name": "수열의 극한"},
    {"concept_id": "C-CALC-002", "curriculum_id": "CALC", "concept_name": "무한급수"},
    {"concept_id": "C-CALC-003", "curriculum_id": "CALC", "concept_name": "초월함수의 미분"},
    {"concept_id": "C-CALC-004", "curriculum_id": "CALC", "concept_name": "몫의 미분법"},
    {"concept_id": "C-CALC-005", "curriculum_id": "CALC", "concept_name": "합성함수 미분법"},
    {"concept_id": "C-CALC-006", "curriculum_id": "CALC", "concept_name": "치환적분법"},
    {"concept_id": "C-CALC-007", "curriculum_id": "CALC", "concept_name": "부분적분법"},

    # PSTAT (확률과 통계)
    {"concept_id": "C-PSTAT-001", "curriculum_id": "PSTAT", "concept_name": "원순열"},
    {"concept_id": "C-PSTAT-002", "curriculum_id": "PSTAT", "concept_name": "중복순열/조합"},
    {"concept_id": "C-PSTAT-003", "curriculum_id": "PSTAT", "concept_name": "이항정리"},
    {"concept_id": "C-PSTAT-004", "curriculum_id": "PSTAT", "concept_name": "조건부확률"},
    {"concept_id": "C-PSTAT-005", "curriculum_id": "PSTAT", "concept_name": "이산/연속 확률분포"},
    {"concept_id": "C-PSTAT-006", "curriculum_id": "PSTAT", "concept_name": "통계적 추정"},

    # GEO (기하)
    {"concept_id": "C-GEO-001", "curriculum_id": "GEO", "concept_name": "포물선"},
    {"concept_id": "C-GEO-002", "curriculum_id": "GEO", "concept_name": "타원"},
    {"concept_id": "C-GEO-003", "curriculum_id": "GEO", "concept_name": "쌍곡선"},
    {"concept_id": "C-GEO-004", "curriculum_id": "GEO", "concept_name": "벡터의 연산"},
    {"concept_id": "C-GEO-005", "curriculum_id": "GEO", "concept_name": "벡터의 내적"},
    {"concept_id": "C-GEO-006", "curriculum_id": "GEO", "concept_name": "공간도형과 공간좌표"},
]

concept_relations = [
    # M-ALL
    {"from_concept_id": "C-MALL-003", "to_concept_id": "C-MALL-002", "relation_type": "REQUIRES"}, # C_일차방정식 → REQUIRES → C_정수와유리수
    {"from_concept_id": "C-MALL-005", "to_concept_id": "C-MALL-004", "relation_type": "REQUIRES"}, # C_인수분해 → REQUIRES → C_다항식의연산
    {"from_concept_id": "C-HCOM-001", "to_concept_id": "C-MALL-005", "relation_type": "REQUIRES"}, # (고등) C_다항식(고) → REQUIRES → C_인수분해(중)
    {"from_concept_id": "C-MALL-008", "to_concept_id": "C-MALL-003", "relation_type": "REQUIRES"}, # C_일차함수 → REQUIRES → C_일차방정식
    {"from_concept_id": "C-MALL-009", "to_concept_id": "C-MALL-005", "relation_type": "REQUIRES"}, # C_이차함수 → REQUIRES → C_인수분해
    {"from_concept_id": "C-HCOM-012", "to_concept_id": "C-MALL-009", "relation_type": "REQUIRES"}, # (고등) C_함수(고) → REQUIRES → C_이차함수(중)
    {"from_concept_id": "C-MALL-013", "to_concept_id": "C-MALL-011", "relation_type": "REQUIRES"}, # C_피타고라스 → REQUIRES → C_삼각형의성질
    {"from_concept_id": "C-MALL-014", "to_concept_id": "C-MALL-013", "relation_type": "REQUIRES"}, # C_삼각비 → REQUIRES → C_피타고라스
    {"from_concept_id": "C-MATH1-005", "to_concept_id": "C-MALL-014", "relation_type": "EXPANDS"}, # (고등) C_삼각함수(수1) → REQUIRES → C_삼각비(중)
    {"from_concept_id": "C-HCOM-015", "to_concept_id": "C-MALL-015", "relation_type": "REQUIRES"}, # (고등) C_순열과조합(고) → REQUIRES → C_경우의수(중)
    {"from_concept_id": "C-HCOM-016", "to_concept_id": "C-MALL-015", "relation_type": "REQUIRES"}, # (고등) C_순열과조합(고) → REQUIRES → C_경우의수(중)

    # H-COMMON
    {"from_concept_id": "C-HCOM-001", "to_concept_id": "C-MALL-004", "relation_type": "REQUIRES"}, # C_나머지정리 → REQUIRES → C_다항식의연산(중)
    {"from_concept_id": "C-HCOM-003", "to_concept_id": "C-MALL-001", "relation_type": "REQUIRES"}, # C_복소수 → REQUIRES → C_제곱근(중) (using 소인수분해 as proxy)
    {"from_concept_id": "C-HCOM-005", "to_concept_id": "C-MALL-009", "relation_type": "LINKS"}, # C_이차함수와관계 → LINKS → C_이차함수(중)
    {"from_concept_id": "C-HCOM-005", "to_concept_id": "C-HCOM-004", "relation_type": "LINKS"}, # C_이차함수와관계 → LINKS → C_이차방정식
    {"from_concept_id": "C-HCOM-008", "to_concept_id": "C-MALL-013", "relation_type": "LINKS"}, # C_원의방정식 → LINKS → C_피타고라스(중)
    {"from_concept_id": "C-HCOM-008", "to_concept_id": "C-MALL-009", "relation_type": "LINKS"}, # C_원의방정식 → LINKS → C_이차함수(중)
    {"from_concept_id": "C-HCOM-013", "to_concept_id": "C-HCOM-012", "relation_type": "REQUIRES"}, # C_합성/역함수 → REQUIRES → C_함수
    {"from_concept_id": "C-HCOM-015", "to_concept_id": "C-MALL-015", "relation_type": "REQUIRES"}, # C_순열과조합 → REQUIRES → C_경우의수(중)

    # MATH-I
    {"from_concept_id": "C-MATH1-003", "to_concept_id": "C-MATH1-002", "relation_type": "REQUIRES"}, # C_로그함수 → REQUIRES → C_지수함수 (assuming both are covered by C-MATH1-003)
    {"from_concept_id": "C-MATH1-003", "to_concept_id": "C-MALL-001", "relation_type": "REQUIRES"}, # C_지수함수 → REQUIRES → C_지수법칙(중) (using 소인수분해 as proxy)
    {"from_concept_id": "C-MATH1-005", "to_concept_id": "C-MALL-014", "relation_type": "EXPANDS"}, # C_삼각함수 → EXPANDS → C_삼각비(중)
    {"from_concept_id": "C-MATH1-004", "to_concept_id": "C-MALL-013", "relation_type": "EXPANDS"}, # C_코사인법칙 → EXPANDS → C_피타고라스(중)

    # MATH-II
    {"from_concept_id": "C-MATH2-003", "to_concept_id": "C-MATH2-001", "relation_type": "REQUIRES"}, # C_미분계수 → REQUIRES → C_함수의극한
    {"from_concept_id": "C-MATH2-006", "to_concept_id": "C-MATH2-004", "relation_type": "REQUIRES"}, # C_극대극소 → REQUIRES → C_도함수
    {"from_concept_id": "C-MATH2-007", "to_concept_id": "C-MATH2-004", "relation_type": "REVERSE_OF"}, # C_부정적분 → REVERSE_OF → C_도함수
    {"from_concept_id": "C-MATH2-009", "to_concept_id": "C-MATH2-008", "relation_type": "REQUIRES"}, # C_정적분넓이 → REQUIRES → C_정적분

    # CALC
    {"from_concept_id": "C-CALC-002", "to_concept_id": "C-MATH1-007", "relation_type": "REQUIRES"}, # C_무한급수 → REQUIRES → C_수열(수1)
    {"from_concept_id": "C-CALC-003", "to_concept_id": "C-MATH2-004", "relation_type": "REQUIRES"}, # C_초월함수미분 → REQUIRES → C_도함수(수2)
    {"from_concept_id": "C-CALC-003", "to_concept_id": "C-MATH1-003", "relation_type": "REQUIRES"}, # C_초월함수미분 → REQUIRES → C_지수/로그/삼각(수1)
    {"from_concept_id": "C-CALC-006", "to_concept_id": "C-MATH2-007", "relation_type": "REQUIRES"}, # C_치환/부분적분 → REQUIRES → C_부정적분(수2)
    {"from_concept_id": "C-CALC-007", "to_concept_id": "C-MATH2-007", "relation_type": "REQUIRES"}, # C_치환/부분적분 → REQUIRES → C_부정적분(수2)

    # PSTAT
    {"from_concept_id": "C-PSTAT-002", "to_concept_id": "C-HCOM-016", "relation_type": "REQUIRES"}, # C_중복조합 → REQUIRES → C_조합(고하)
    {"from_concept_id": "C-PSTAT-004", "to_concept_id": "C-MALL-016", "relation_type": "REQUIRES"}, # C_조건부확률 → REQUIRES → C_확률(중)

    # GEO
    {"from_concept_id": "C-GEO-001", "to_concept_id": "C-HCOM-008", "relation_type": "REQUIRES"}, # C_이차곡선 → REQUIRES → C_원의방정식(고상)
    {"from_concept_id": "C-GEO-002", "to_concept_id": "C-HCOM-008", "relation_type": "REQUIRES"}, # C_이차곡선 → REQUIRES → C_원의방정식(고상)
    {"from_concept_id": "C-GEO-003", "to_concept_id": "C-HCOM-008", "relation_type": "REQUIRES"}, # C_이차곡선 → REQUIRES → C_원의방정식(고상)
]

def populate():
    for curr in curriculums:
        if not db.query(models.Curriculum).filter_by(curriculum_id=curr["curriculum_id"]).first():
            db.add(models.Curriculum(**curr))

    for conc in concepts:
        if not db.query(models.ConceptsLibrary).filter_by(concept_id=conc["concept_id"]).first():
            db.add(models.ConceptsLibrary(**conc))
    
    for rel in concept_relations:
        if not db.query(models.ConceptRelation).filter_by(
            from_concept_id=rel["from_concept_id"],
            to_concept_id=rel["to_concept_id"],
            relation_type=rel["relation_type"]
        ).first():
            db.add(models.ConceptRelation(**rel))

    db.commit()
    print("Database populated with curriculums, concepts, and concept relations.")

if __name__ == "__main__":
    populate()
