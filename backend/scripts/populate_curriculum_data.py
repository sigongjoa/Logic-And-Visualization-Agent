import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Base, Curriculum, ConceptsLibrary, ConceptRelation

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

def populate_curriculum_data():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Define curriculum data
        curriculums_data = [
            {"curriculum_id": "M-ALL", "curriculum_name": "중등 수학: 공통 기초", "description": ""},
            {"curriculum_id": "H-COMMON", "curriculum_name": "고등 수학 (상), (하)", "description": ""},
            {"curriculum_id": "MATH-I", "curriculum_name": "수학 I", "description": ""},
            {"curriculum_id": "MATH-II", "curriculum_name": "수학 II", "description": ""},
            {"curriculum_id": "CALC", "curriculum_name": "미적분", "description": ""},
            {"curriculum_id": "PSTAT", "curriculum_name": "확률과 통계", "description": ""},
            {"curriculum_id": "GEO", "curriculum_name": "기하", "description": ""},
        ]

        # Define concepts library data
        concepts_data = [
            # M-ALL
            {"concept_id": "C-M-ALL-001", "curriculum_id": "M-ALL", "concept_name": "소인수분해", "manim_data_path": None, "description": ""},
            {"concept_id": "C-M-ALL-002", "curriculum_id": "M-ALL", "concept_name": "정수와 유리수", "manim_data_path": None, "description": ""},
            {"concept_id": "C-M-ALL-003", "curriculum_id": "M-ALL", "concept_name": "일차방정식의 풀이", "manim_data_path": None, "description": ""},
            {"concept_id": "C-M-ALL-004", "curriculum_id": "M-ALL", "concept_name": "다항식의 연산", "manim_data_path": None, "description": "(핵심) 덧셈, 뺄셈, 곱셈"},
            {"concept_id": "C-M-ALL-005", "curriculum_id": "M-ALL", "concept_name": "곱셈 공식 및 인수분해", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-M-ALL-006", "curriculum_id": "M-ALL", "concept_name": "좌표평면과 그래프", "manim_data_path": None, "description": ""},
            {"concept_id": "C-M-ALL-007", "curriculum_id": "M-ALL", "concept_name": "정비례와 반비례", "manim_data_path": None, "description": ""},
            {"concept_id": "C-M-ALL-008", "curriculum_id": "M-ALL", "concept_name": "일차함수와 그래프", "manim_data_path": None, "description": "(핵심) 기울기, y절편"},
            {"concept_id": "C-M-ALL-009", "curriculum_id": "M-ALL", "concept_name": "이차함수와 그래프", "manim_data_path": None, "description": "(핵심) 표준형, 일반형"},
            {"concept_id": "C-M-ALL-010", "curriculum_id": "M-ALL", "concept_name": "기본 도형", "manim_data_path": None, "description": "점, 선, 면, 각"},
            {"concept_id": "C-M-ALL-011", "curriculum_id": "M-ALL", "concept_name": "삼각형/사각형의 성질", "manim_data_path": None, "description": ""},
            {"concept_id": "C-M-ALL-012", "curriculum_id": "M-ALL", "concept_name": "도형의 닮음", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-M-ALL-013", "curriculum_id": "M-ALL", "concept_name": "피타고라스의 정리", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-M-ALL-014", "curriculum_id": "M-ALL", "concept_name": "삼각비", "manim_data_path": None, "description": "(핵심) sin, cos, tan"},
            {"concept_id": "C-M-ALL-015", "curriculum_id": "M-ALL", "concept_name": "경우의 수", "manim_data_path": None, "description": "합/곱의 법칙"},
            {"concept_id": "C-M-ALL-016", "curriculum_id": "M-ALL", "concept_name": "확률의 기본 성질", "manim_data_path": None, "description": ""},

            # H-COMMON
            {"concept_id": "C-H-COMMON-001", "curriculum_id": "H-COMMON", "concept_name": "항등식과 나머지 정리", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-H-COMMON-002", "curriculum_id": "H-COMMON", "concept_name": "인수분해 (고차식)", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-H-COMMON-003", "curriculum_id": "H-COMMON", "concept_name": "복소수", "manim_data_path": None, "description": "i의 정의"},
            {"concept_id": "C-H-COMMON-004", "curriculum_id": "H-COMMON", "concept_name": "이차방정식", "manim_data_path": None, "description": "(핵심) 근의 공식, 판별식"},
            {"concept_id": "C-H-COMMON-005", "curriculum_id": "H-COMMON", "concept_name": "이차함수와 이차방정식의 관계", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-H-COMMON-006", "curriculum_id": "H-COMMON", "concept_name": "여러 가지 방정식", "manim_data_path": None, "description": "3/4차, 연립"},
            {"concept_id": "C-H-COMMON-007", "curriculum_id": "H-COMMON", "concept_name": "평면좌표", "manim_data_path": None, "description": "두 점 사이의 거리"},
            {"concept_id": "C-H-COMMON-008", "curriculum_id": "H-COMMON", "concept_name": "직선의 방정식", "manim_data_path": None, "description": ""},
            {"concept_id": "C-H-COMMON-009", "curriculum_id": "H-COMMON", "concept_name": "원의 방정식", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-H-COMMON-010", "curriculum_id": "H-COMMON", "concept_name": "도형의 이동", "manim_data_path": None, "description": "평행/대칭이동"},
            {"concept_id": "C-H-COMMON-011", "curriculum_id": "H-COMMON", "concept_name": "집합의 연산", "manim_data_path": None, "description": ""},
            {"concept_id": "C-H-COMMON-012", "curriculum_id": "H-COMMON", "concept_name": "명제", "manim_data_path": None, "description": "필요/충분조건"},
            {"concept_id": "C-H-COMMON-013", "curriculum_id": "H-COMMON", "concept_name": "함수 (고등)", "manim_data_path": None, "description": "(핵심) 일대일, 항등, 상수"},
            {"concept_id": "C-H-COMMON-014", "curriculum_id": "H-COMMON", "concept_name": "합성함수와 역함수", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-H-COMMON-015", "curriculum_id": "H-COMMON", "concept_name": "유리함수와 무리함수", "manim_data_path": None, "description": ""},
            {"concept_id": "C-H-COMMON-016", "curriculum_id": "H-COMMON", "concept_name": "순열 (nPr)", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-H-COMMON-017", "curriculum_id": "H-COMMON", "concept_name": "조합 (nCr)", "manim_data_path": None, "description": "(핵심)"},

            # MATH-I
            {"concept_id": "C-MATH-I-001", "curriculum_id": "MATH-I", "concept_name": "거듭제곱근", "manim_data_path": None, "description": ""},
            {"concept_id": "C-MATH-I-002", "curriculum_id": "MATH-I", "concept_name": "지수/로그의 정의와 성질", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-MATH-I-003", "curriculum_id": "MATH-I", "concept_name": "지수/로그 함수와 그래프", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-MATH-I-004", "curriculum_id": "MATH-I", "concept_name": "일반각과 호도법", "manim_data_path": None, "description": ""},
            {"concept_id": "C-MATH-I-005", "curriculum_id": "MATH-I", "concept_name": "삼각함수 그래프", "manim_data_path": None, "description": "(핵심) 주기, 최대/최소"},
            {"concept_id": "C-MATH-I-006", "curriculum_id": "MATH-I", "concept_name": "사인법칙과 코사인법칙", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-MATH-I-007", "curriculum_id": "MATH-I", "concept_name": "등차/등비수열", "manim_data_path": None, "description": "일반항, 합"},
            {"concept_id": "C-MATH-I-008", "curriculum_id": "MATH-I", "concept_name": "시그마 (Σ)", "manim_data_path": None, "description": "(핵심) 정의와 성질"},
            {"concept_id": "C-MATH-I-009", "curriculum_id": "MATH-I", "concept_name": "수학적 귀납법", "manim_data_path": None, "description": ""},

            # MATH-II
            {"concept_id": "C-MATH-II-001", "curriculum_id": "MATH-II", "concept_name": "함수의 극한", "manim_data_path": None, "description": "(핵심) 우극한/좌극한"},
            {"concept_id": "C-MATH-II-002", "curriculum_id": "MATH-II", "concept_name": "함수의 연속성", "manim_data_path": None, "description": "사이값 정리"},
            {"concept_id": "C-MATH-II-003", "curriculum_id": "MATH-II", "concept_name": "미분계수", "manim_data_path": None, "description": "(핵심) 순간변화율"},
            {"concept_id": "C-MATH-II-004", "curriculum_id": "MATH-II", "concept_name": "도함수", "manim_data_path": None, "description": "(핵심) 다항함수의 미분법"},
            {"concept_id": "C-MATH-II-005", "curriculum_id": "MATH-II", "concept_name": "접선의 방정식", "manim_data_path": None, "description": ""},
            {"concept_id": "C-MATH-II-006", "curriculum_id": "MATH-II", "concept_name": "함수의 증가/감소, 극대/극소", "manim_data_path": None, "description": ""},
            {"concept_id": "C-MATH-II-007", "curriculum_id": "MATH-II", "concept_name": "부정적분", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-MATH-II-008", "curriculum_id": "MATH-II", "concept_name": "정적분", "manim_data_path": None, "description": "(핵심) 미적분의 기본정리"},
            {"concept_id": "C-MATH-II-009", "curriculum_id": "MATH-II", "concept_name": "정적분의 활용 (넓이)", "manim_data_path": None, "description": ""},

            # CALC
            {"concept_id": "C-CALC-001", "curriculum_id": "CALC", "concept_name": "수열의 극한, 무한급수", "manim_data_path": None, "description": ""},
            {"concept_id": "C-CALC-002", "curriculum_id": "CALC", "concept_name": "초월함수의 미분", "manim_data_path": None, "description": "(핵심) 지수, 로그, 삼각"},
            {"concept_id": "C-CALC-003", "curriculum_id": "CALC", "concept_name": "몫의 미분법, 합성함수 미분법", "manim_data_path": None, "description": ""},
            {"concept_id": "C-CALC-004", "curriculum_id": "CALC", "concept_name": "치환적분법, 부분적분법", "manim_data_path": None, "description": "(핵심)"},

            # PSTAT
            {"concept_id": "C-PSTAT-001", "curriculum_id": "PSTAT", "concept_name": "원순열, 중복순열/조합", "manim_data_path": None, "description": ""},
            {"concept_id": "C-PSTAT-002", "curriculum_id": "PSTAT", "concept_name": "이항정리", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-PSTAT-003", "curriculum_id": "PSTAT", "concept_name": "조건부확률", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-PSTAT-004", "curriculum_id": "PSTAT", "concept_name": "이산/연속 확률분포", "manim_data_path": None, "description": ""},
            {"concept_id": "C-PSTAT-005", "curriculum_id": "PSTAT", "concept_name": "통계적 추정 (신뢰구간)", "manim_data_path": None, "description": ""},

            # GEO
            {"concept_id": "C-GEO-001", "curriculum_id": "GEO", "concept_name": "포물선, 타원, 쌍곡선의 정의와 방정식", "manim_data_path": None, "description": ""},
            {"concept_id": "C-GEO-002", "curriculum_id": "GEO", "concept_name": "벡터의 연산", "manim_data_path": None, "description": "(핵심) 덧셈, 뺄셈, 실수배"},
            {"concept_id": "C-GEO-003", "curriculum_id": "GEO", "concept_name": "벡터의 내적", "manim_data_path": None, "description": "(핵심)"},
            {"concept_id": "C-GEO-004", "curriculum_id": "GEO", "concept_name": "공간도형과 공간좌표", "manim_data_path": None, "description": ""},
        ]

        # Define concept relations data
        concept_relations_data = [
            # M-ALL
            {"from_concept_id": "C-M-ALL-003", "to_concept_id": "C-M-ALL-002", "relation_type": "REQUIRES"}, # C_일차방정식 → REQUIRES → C_정수와유리수
            {"from_concept_id": "C-M-ALL-005", "to_concept_id": "C-M-ALL-004", "relation_type": "REQUIRES"}, # C_인수분해 → REQUIRES → C_다항식의연산
            {"from_concept_id": "C-H-COMMON-002", "to_concept_id": "C-M-ALL-005", "relation_type": "REQUIRES"}, # (고등) C_다항식(고) → REQUIRES → C_인수분해(중) - Assuming C-H-COMMON-002 is high school polynomial
            {"from_concept_id": "C-M-ALL-008", "to_concept_id": "C-M-ALL-003", "relation_type": "REQUIRES"}, # C_일차함수 → REQUIRES → C_일차방정식
            {"from_concept_id": "C-M-ALL-009", "to_concept_id": "C-M-ALL-005", "relation_type": "REQUIRES"}, # C_이차함수 → REQUIRES → C_인수분해
            {"from_concept_id": "C-H-COMMON-005", "to_concept_id": "C-M-ALL-009", "relation_type": "REQUIRES"}, # (고등) C_함수(고) → REQUIRES → C_이차함수(중) - Assuming C-H-COMMON-005 is high school function
            {"from_concept_id": "C-M-ALL-013", "to_concept_id": "C-M-ALL-011", "relation_type": "REQUIRES"}, # C_피타고라스 → REQUIRES → C_삼각형의성질
            {"from_concept_id": "C-M-ALL-014", "to_concept_id": "C-M-ALL-013", "relation_type": "REQUIRES"}, # C_삼각비 → REQUIRES → C_피타고라스
            {"from_concept_id": "C-MATH-I-005", "to_concept_id": "C-M-ALL-014", "relation_type": "REQUIRES"}, # (고등) C_삼각함수(수1) → REQUIRES → C_삼각비(중) - Assuming C-MATH-I-005 is high school trig function
            {"from_concept_id": "C-PSTAT-001", "to_concept_id": "C-M-ALL-015", "relation_type": "REQUIRES"}, # (고등) C_순열과조합(고) → REQUIRES → C_경우의수(중) - Assuming C-PSTAT-001 is high school permutation/combination

            # H-COMMON
            {"from_concept_id": "C-H-COMMON-001", "to_concept_id": "C-M-ALL-004", "relation_type": "REQUIRES"}, # C_나머지정리 → REQUIRES → C_다항식의연산(중)
            {"from_concept_id": "C-H-COMMON-003", "to_concept_id": "C-M-ALL-001", "relation_type": "REQUIRES"}, # C_복소수 → REQUIRES → C_제곱근(중) - Assuming C-M-ALL-001 is related to square roots
            {"from_concept_id": "C-H-COMMON-005", "to_concept_id": "C-M-ALL-009", "relation_type": "LINKS"}, # C_이차함수와관계 → LINKS → C_이차함수(중)
            {"from_concept_id": "C-H-COMMON-005", "to_concept_id": "C-H-COMMON-004", "relation_type": "LINKS"}, # C_이차함수와관계 → LINKS → C_이차방정식
            {"from_concept_id": "C-H-COMMON-009", "to_concept_id": "C-M-ALL-013", "relation_type": "LINKS"}, # C_원의방정식 → LINKS → C_피타고라스(중)
            {"from_concept_id": "C-H-COMMON-009", "to_concept_id": "C-M-ALL-009", "relation_type": "LINKS"}, # C_원의방정식 → LINKS → C_이차함수(중)
            {"from_concept_id": "C-H-COMMON-014", "to_concept_id": "C-H-COMMON-013", "relation_type": "REQUIRES"}, # C_합성/역함수 → REQUIRES → C_함수
            {"from_concept_id": "C-H-COMMON-016", "to_concept_id": "C-M-ALL-015", "relation_type": "REQUIRES"}, # C_순열과조합 → REQUIRES → C_경우의수(중) - Assuming C-H-COMMON-016 is permutation/combination

            # MATH-I
            {"from_concept_id": "C-MATH-I-003", "to_concept_id": "C-MATH-I-002", "relation_type": "REQUIRES"}, # C_로그함수 → REQUIRES → C_지수함수 - Assuming C-MATH-I-003 is log function, C-MATH-I-002 is exp function
            {"from_concept_id": "C-MATH-I-002", "to_concept_id": "C-M-ALL-004", "relation_type": "REQUIRES"}, # C_지수함수 → REQUIRES → C_지수법칙(중) - Assuming C-M-ALL-004 is related to exponent rules
            {"from_concept_id": "C-MATH-I-005", "to_concept_id": "C-M-ALL-014", "relation_type": "EXPANDS"}, # C_삼각함수 → EXPANDS → C_삼각비(중)
            {"from_concept_id": "C-MATH-I-006", "to_concept_id": "C-M-ALL-013", "relation_type": "EXPANDS"}, # C_코사인법칙 → EXPANDS → C_피타고라스(중)

            # MATH-II
            {"from_concept_id": "C-MATH-II-003", "to_concept_id": "C-MATH-II-001", "relation_type": "REQUIRES"}, # C_미분계수 → REQUIRES → C_함수의극한
            {"from_concept_id": "C-MATH-II-006", "to_concept_id": "C-MATH-II-004", "relation_type": "REQUIRES"}, # C_극대극소 → REQUIRES → C_도함수
            {"from_concept_id": "C-MATH-II-007", "to_concept_id": "C-MATH-II-004", "relation_type": "REVERSE_OF"}, # C_부정적분 → REVERSE_OF → C_도함수
            {"from_concept_id": "C-MATH-II-009", "to_concept_id": "C-MATH-II-008", "relation_type": "REQUIRES"}, # C_정적분넓이 → REQUIRES → C_정적분

            # CALC
            {"from_concept_id": "C-CALC-001", "to_concept_id": "C-MATH-I-007", "relation_type": "REQUIRES"}, # C_무한급수 → REQUIRES → C_수열(수1)
            {"from_concept_id": "C-CALC-002", "to_concept_id": "C-MATH-II-004", "relation_type": "REQUIRES"}, # C_초월함수미분 → REQUIRES → C_도함수(수2)
            {"from_concept_id": "C-CALC-002", "to_concept_id": "C-MATH-I-003", "relation_type": "REQUIRES"}, # C_초월함수미분 → REQUIRES → C_지수/로그/삼각(수1) - Assuming C-MATH-I-003 is exp/log/trig functions
            {"from_concept_id": "C-CALC-004", "to_concept_id": "C-MATH-II-007", "relation_type": "REQUIRES"}, # C_치환/부분적분 → REQUIRES → C_부정적분(수2)

            # PSTAT
            {"from_concept_id": "C-PSTAT-001", "to_concept_id": "C-H-COMMON-017", "relation_type": "REQUIRES"}, # C_중복조합 → REQUIRES → C_조합(고하) - Assuming C-PSTAT-001 is combination
            {"from_concept_id": "C-PSTAT-003", "to_concept_id": "C-M-ALL-016", "relation_type": "REQUIRES"}, # C_조건부확률 → REQUIRES → C_확률(중)

            # GEO
            {"from_concept_id": "C-GEO-001", "to_concept_id": "C-H-COMMON-009", "relation_type": "REQUIRES"}, # C_이차곡선 → REQUIRES → C_원의방정식(고상)
        ]


        # Insert curriculums
        for data in curriculums_data:
            if not db.query(Curriculum).filter_by(curriculum_id=data["curriculum_id"]).first():
                db.add(Curriculum(**data))
        db.commit()

        # Insert concepts
        for data in concepts_data:
            if not db.query(ConceptsLibrary).filter_by(concept_id=data["concept_id"]).first():
                db.add(ConceptsLibrary(**data))
        db.commit()

        # Insert concept relations
        for data in concept_relations_data:
            # Check if both concepts exist before adding relation
            from_concept = db.query(ConceptsLibrary).filter_by(concept_id=data["from_concept_id"]).first()
            to_concept = db.query(ConceptsLibrary).filter_by(concept_id=data["to_concept_id"]).first()
            if from_concept and to_concept:
                if not db.query(ConceptRelation).filter_by(
                    from_concept_id=data["from_concept_id"],
                    to_concept_id=data["to_concept_id"],
                    relation_type=data["relation_type"]
                ).first():
                    db.add(ConceptRelation(**data))
            else:
                print(f"Warning: Skipping relation {data} due to missing concept(s).")
        db.commit()

        print("Curriculum and concept data populated successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error populating data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_curriculum_data()
