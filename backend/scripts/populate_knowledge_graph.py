from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Curriculum, ConceptsLibrary, ConceptRelation
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def populate_knowledge_graph(db):
    try:
        # Clear existing data (optional, for development)
        db.query(ConceptRelation).delete()
        db.query(ConceptsLibrary).delete()
        db.query(Curriculum).delete()
        db.commit()

        # 1. Curriculums
        curriculums_data = [
            {"curriculum_id": "M-ALL", "curriculum_name": "중등 수학: 공통 기초", "description": "4축 모델의 '인지 기저'를 형성하는 가장 근본적인 뿌리입니다."},
            {"curriculum_id": "H-COMMON", "curriculum_name": "고등 수학 (상), (하)", "description": "중등 기초를 '통합'하고 '심화'시키는 가장 중요한 허리입니다."},
            {"curriculum_id": "MATH-I", "curriculum_name": "수학 I", "description": "고등 수학 선택 과목: 수학 I"},
            {"curriculum_id": "MATH-II", "curriculum_name": "수학 II", "description": "고등 수학 선택 과목: 수학 II"},
            {"curriculum_id": "CALC", "curriculum_name": "미적분", "description": "고등 수학 선택 과목: 미적분"},
            {"curriculum_id": "PSTAT", "curriculum_name": "확률과 통계", "description": "고등 수학 선택 과목: 확률과 통계"},
            {"curriculum_id": "GEO", "curriculum_name": "기하", "description": "고등 수학 선택 과목: 기하"},
        ]
        for data in curriculums_data:
            db.add(Curriculum(**data))
        db.commit()

        # 2. Concepts_Library (Nodes)
        concepts_data = [
            # M-ALL
            {"concept_id": "C_소인수분해", "curriculum_id": "M-ALL", "concept_name": "소인수분해", "manim_data_path": "manim/M-ALL/소인수분해.mp4"},
            {"concept_id": "C_정수와유리수", "curriculum_id": "M-ALL", "concept_name": "정수와 유리수", "manim_data_path": "manim/M-ALL/정수와유리수.mp4"},
            {"concept_id": "C_일차방정식의풀이", "curriculum_id": "M-ALL", "concept_name": "일차방정식의 풀이", "manim_data_path": "manim/M-ALL/일차방정식의풀이.mp4"},
            {"concept_id": "C_다항식의연산", "curriculum_id": "M-ALL", "concept_name": "다항식의 연산", "manim_data_path": "manim/M-ALL/다항식의연산.mp4"},
            {"concept_id": "C_곱셈공식및인수분해", "curriculum_id": "M-ALL", "concept_name": "곱셈 공식 및 인수분해", "manim_data_path": "manim/M-ALL/곱셈공식및인수분해.mp4"},
            {"concept_id": "C_좌표평면과그래프", "curriculum_id": "M-ALL", "concept_name": "좌표평면과 그래프", "manim_data_path": "manim/M-ALL/좌표평면과그래프.mp4"},
            {"concept_id": "C_정비례와반비례", "curriculum_id": "M-ALL", "concept_name": "정비례와 반비례", "manim_data_path": "manim/M-ALL/정비례와반비례.mp4"},
            {"concept_id": "C_일차함수와그래프", "curriculum_id": "M-ALL", "concept_name": "일차함수와 그래프", "manim_data_path": "manim/M-ALL/일차함수와그래프.mp4"},
            {"concept_id": "C_이차함수와그래프", "curriculum_id": "M-ALL", "concept_name": "이차함수와 그래프", "manim_data_path": "manim/M-ALL/이차함수와그래프.mp4"},
            {"concept_id": "C_기본도형", "curriculum_id": "M-ALL", "concept_name": "기본 도형", "manim_data_path": "manim/M-ALL/기본도형.mp4"},
            {"concept_id": "C_삼각형사각형의성질", "curriculum_id": "M-ALL", "concept_name": "삼각형/사각형의 성질", "manim_data_path": "manim/M-ALL/삼각형사각형의성질.mp4"},
            {"concept_id": "C_도형의닮음", "curriculum_id": "M-ALL", "concept_name": "도형의 닮음", "manim_data_path": "manim/M-ALL/도형의닮음.mp4"},
            {"concept_id": "C_피타고라스의정리", "curriculum_id": "M-ALL", "concept_name": "피타고라스의 정리", "manim_data_path": "manim/M-ALL/피타고라스의정리.mp4"},
            {"concept_id": "C_삼각비", "curriculum_id": "M-ALL", "concept_name": "삼각비", "manim_data_path": "manim/M-ALL/삼각비.mp4"},
            {"concept_id": "C_경우의수", "curriculum_id": "M-ALL", "concept_name": "경우의 수", "manim_data_path": "manim/M-ALL/경우의수.mp4"},
            {"concept_id": "C_확률의기본성질", "curriculum_id": "M-ALL", "concept_name": "확률의 기본 성질", "manim_data_path": "manim/M-ALL/확률의기본성질.mp4"},
            {"concept_id": "C_제곱근", "curriculum_id": "M-ALL", "concept_name": "제곱근", "manim_data_path": "manim/M-ALL/제곱근.mp4"}, # Added missing concept
            
            # H-COMMON
            {"concept_id": "C_항등식과나머지정리", "curriculum_id": "H-COMMON", "concept_name": "항등식과 나머지 정리", "manim_data_path": "manim/H-COMMON/항등식과나머지정리.mp4"},
            {"concept_id": "C_인수분해고차식", "curriculum_id": "H-COMMON", "concept_name": "인수분해 (고차식)", "manim_data_path": "manim/H-COMMON/인수분해고차식.mp4"},
            {"concept_id": "C_복소수", "curriculum_id": "H-COMMON", "concept_name": "복소수", "manim_data_path": "manim/H-COMMON/복소수.mp4"},
            {"concept_id": "C_다항식고", "curriculum_id": "H-COMMON", "concept_name": "다항식(고)", "manim_data_path": "manim/H-COMMON/다항식고.mp4"}, # Added missing concept
            {"concept_id": "C_순열과조합고", "curriculum_id": "H-COMMON", "concept_name": "순열과 조합(고)", "manim_data_path": "manim/H-COMMON/순열과조합고.mp4"}, # Added missing concept
            {"concept_id": "C_이차방정식", "curriculum_id": "H-COMMON", "concept_name": "이차방정식", "manim_data_path": "manim/H-COMMON/이차방정식.mp4"},
            {"concept_id": "C_이차함수와이차방정식의관계", "curriculum_id": "H-COMMON", "concept_name": "이차함수와 이차방정식의 관계", "manim_data_path": "manim/H-COMMON/이차함수와이차방정식의관계.mp4"},
            {"concept_id": "C_여러가지방정식", "curriculum_id": "H-COMMON", "concept_name": "여러 가지 방정식", "manim_data_path": "manim/H-COMMON/여러가지방정식.mp4"},
            {"concept_id": "C_평면좌표", "curriculum_id": "H-COMMON", "concept_name": "평면좌표", "manim_data_path": "manim/H-COMMON/평면좌표.mp4"},
            {"concept_id": "C_직선의방정식", "curriculum_id": "H-COMMON", "concept_name": "직선의 방정식", "manim_data_path": "manim/H-COMMON/직선의방정식.mp4"},
            {"concept_id": "C_원의방정식", "curriculum_id": "H-COMMON", "concept_name": "원의 방정식", "manim_data_path": "manim/H-COMMON/원의방정식.mp4"},
            {"concept_id": "C_도형의이동", "curriculum_id": "H-COMMON", "concept_name": "도형의 이동", "manim_data_path": "manim/H-COMMON/도형의이동.mp4"},
            {"concept_id": "C_집합의연산", "curriculum_id": "H-COMMON", "concept_name": "집합의 연산", "manim_data_path": "manim/H-COMMON/집합의연산.mp4"},
            {"concept_id": "C_명제", "curriculum_id": "H-COMMON", "concept_name": "명제", "manim_data_path": "manim/H-COMMON/명제.mp4"},
            {"concept_id": "C_함수", "curriculum_id": "H-COMMON", "concept_name": "함수", "manim_data_path": "manim/H-COMMON/함수.mp4"},
            {"concept_id": "C_합성함수와역함수", "curriculum_id": "H-COMMON", "concept_name": "합성함수와 역함수", "manim_data_path": "manim/H-COMMON/합성함수와역함수.mp4"},
            {"concept_id": "C_유리함수와무리함수", "curriculum_id": "H-COMMON", "concept_name": "유리함수와 무리함수", "manim_data_path": "manim/H-COMMON/유리함수와무리함수.mp4"},
            {"concept_id": "C_순열", "curriculum_id": "H-COMMON", "concept_name": "순열", "manim_data_path": "manim/H-COMMON/순열.mp4"},
            {"concept_id": "C_조합", "curriculum_id": "H-COMMON", "concept_name": "조합", "manim_data_path": "manim/H-COMMON/조합.mp4"},

            # MATH-I
            {"concept_id": "C_거듭제곱근", "curriculum_id": "MATH-I", "concept_name": "거듭제곱근", "manim_data_path": "manim/MATH-I/거듭제곱근.mp4"},
            {"concept_id": "C_지수로그의정의와성질", "curriculum_id": "MATH-I", "concept_name": "지수/로그의 정의와 성질", "manim_data_path": "manim/MATH-I/지수로그의정의와성질.mp4"},
            {"concept_id": "C_지수로그함수와그래프", "curriculum_id": "MATH-I", "concept_name": "지수/로그 함수와 그래프", "manim_data_path": "manim/MATH-I/지수로그함수와그래프.mp4"},
            {"concept_id": "C_일반각과호도법", "curriculum_id": "MATH-I", "concept_name": "일반각과 호도법", "manim_data_path": "manim/MATH-I/일반각과호도법.mp4"},
            {"concept_id": "C_삼각함수그래프", "curriculum_id": "MATH-I", "concept_name": "삼각함수 그래프", "manim_data_path": "manim/MATH-I/삼각함수그래프.mp4"},
            {"concept_id": "C_사인법칙과코사인법칙", "curriculum_id": "MATH-I", "concept_name": "사인법칙과 코사인법칙", "manim_data_path": "manim/MATH-I/사인법칙과코사인법칙.mp4"},
            {"concept_id": "C_등차등비수열", "curriculum_id": "MATH-I", "concept_name": "등차/등비수열", "manim_data_path": "manim/MATH-I/등차등비수열.mp4"},
            {"concept_id": "C_시그마의정의와성질", "curriculum_id": "MATH-I", "concept_name": "시그마의 정의와 성질", "manim_data_path": "manim/MATH-I/시그마의정의와성질.mp4"},
            {"concept_id": "C_수학적귀납법", "curriculum_id": "MATH-I", "concept_name": "수학적 귀납법", "manim_data_path": "manim/MATH-I/수학적귀납법.mp4"},

            # MATH-II
            {"concept_id": "C_함수의극한", "curriculum_id": "MATH-II", "concept_name": "함수의 극한", "manim_data_path": "manim/MATH-II/함수의극한.mp4"},
            {"concept_id": "C_함수의연속성", "curriculum_id": "MATH-II", "concept_name": "함수의 연속성", "manim_data_path": "manim/MATH-II/함수의연속성.mp4"},
            {"concept_id": "C_미분계수", "curriculum_id": "MATH-II", "concept_name": "미분계수", "manim_data_path": "manim/MATH-II/미분계수.mp4"},
            {"concept_id": "C_도함수", "curriculum_id": "MATH-II", "concept_name": "도함수", "manim_data_path": "manim/MATH-II/도함수.mp4"},
            {"concept_id": "C_접선의방정식", "curriculum_id": "MATH-II", "concept_name": "접선의 방정식", "manim_data_path": "manim/MATH-II/접선의방정식.mp4"},
            {"concept_id": "C_함수의증가감소극대극소", "curriculum_id": "MATH-II", "concept_name": "함수의 증가/감소, 극대/극소", "manim_data_path": "manim/MATH-II/함수의증가감소극대극소.mp4"},
            {"concept_id": "C_부정적분", "curriculum_id": "MATH-II", "concept_name": "부정적분", "manim_data_path": "manim/MATH-II/부정적분.mp4"},
            {"concept_id": "C_정적분", "curriculum_id": "MATH-II", "concept_name": "정적분", "manim_data_path": "manim/MATH-II/정적분.mp4"},
            {"concept_id": "C_정적분의활용", "curriculum_id": "MATH-II", "concept_name": "정적분의 활용", "manim_data_path": "manim/MATH-II/정적분의활용.mp4"},

            # CALC
            {"concept_id": "C_수열의극한", "curriculum_id": "CALC", "concept_name": "수열의 극한", "manim_data_path": "manim/CALC/수열의극한.mp4"},
            {"concept_id": "C_무한급수", "curriculum_id": "CALC", "concept_name": "무한급수", "manim_data_path": "manim/CALC/무한급수.mp4"},
            {"concept_id": "C_초월함수의미분", "curriculum_id": "CALC", "concept_name": "초월함수의 미분", "manim_data_path": "manim/CALC/초월함수의미분.mp4"},
            {"concept_id": "C_몫의미분법", "curriculum_id": "CALC", "concept_name": "몫의 미분법", "manim_data_path": "manim/CALC/몫의미분법.mp4"},
            {"concept_id": "C_합성함수미분법", "curriculum_id": "CALC", "concept_name": "합성함수 미분법", "manim_data_path": "manim/CALC/합성함수미분법.mp4"},
            {"concept_id": "C_치환적분법", "curriculum_id": "CALC", "concept_name": "치환적분법", "manim_data_path": "manim/CALC/치환적분법.mp4"},
            {"concept_id": "C_부분적분법", "curriculum_id": "CALC", "concept_name": "부분적분법", "manim_data_path": "manim/CALC/부분적분법.mp4"},

            # PSTAT
            {"concept_id": "C_원순열", "curriculum_id": "PSTAT", "concept_name": "원순열", "manim_data_path": "manim/PSTAT/원순열.mp4"},
            {"concept_id": "C_중복순열조합", "curriculum_id": "PSTAT", "concept_name": "중복순열/조합", "manim_data_path": "manim/PSTAT/중복순열조합.mp4"},
            {"concept_id": "C_이항정리", "curriculum_id": "PSTAT", "concept_name": "이항정리", "manim_data_path": "manim/PSTAT/이항정리.mp4"},
            {"concept_id": "C_조건부확률", "curriculum_id": "PSTAT", "concept_name": "조건부확률", "manim_data_path": "manim/PSTAT/조건부확률.mp4"},
            {"concept_id": "C_이산연속확률분포", "curriculum_id": "PSTAT", "concept_name": "이산/연속 확률분포", "manim_data_path": "manim/PSTAT/이산연속확률분포.mp4"},
            {"concept_id": "C_통계적추정", "curriculum_id": "PSTAT", "concept_name": "통계적 추정", "manim_data_path": "manim/PSTAT/통계적추정.mp4"},

            # GEO
            {"concept_id": "C_이차곡선", "curriculum_id": "GEO", "concept_name": "이차곡선", "manim_data_path": "manim/GEO/이차곡선.mp4"},
            {"concept_id": "C_벡터의연산", "curriculum_id": "GEO", "concept_name": "벡터의 연산", "manim_data_path": "manim/GEO/벡터의연산.mp4"},
            {"concept_id": "C_벡터의내적", "curriculum_id": "GEO", "concept_name": "벡터의 내적", "manim_data_path": "manim/GEO/벡터의내적.mp4"},
            {"concept_id": "C_공간도형과공간좌표", "curriculum_id": "GEO", "concept_name": "공간도형과 공간좌표", "manim_data_path": "manim/GEO/공간도형과공간좌표.mp4"},
            {"concept_id": "C_기본개념", "curriculum_id": "M-ALL", "concept_name": "기본개념", "manim_data_path": "manim/M-ALL/기본개념.mp4"}, # Added for test_anki_cards.py
        ]
        for data in concepts_data:
            db.add(ConceptsLibrary(**data))
        db.commit()

        # 3. Concept_Relations (Edges)
        relations_data = [
            # M-ALL
            {"from_concept_id": "C_일차방정식의풀이", "to_concept_id": "C_정수와유리수", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_곱셈공식및인수분해", "to_concept_id": "C_다항식의연산", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_다항식고", "to_concept_id": "C_곱셈공식및인수분해", "relation_type": "REQUIRES"}, # Placeholder for high school concept
            {"from_concept_id": "C_일차함수와그래프", "to_concept_id": "C_일차방정식의풀이", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_이차함수와그래프", "to_concept_id": "C_곱셈공식및인수분해", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_함수고", "to_concept_id": "C_이차함수와그래프", "relation_type": "REQUIRES"}, # Placeholder for high school concept
            {"from_concept_id": "C_피타고라스의정리", "to_concept_id": "C_삼각형사각형의성질", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_삼각비", "to_concept_id": "C_피타고라스의정리", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_삼각함수수1", "to_concept_id": "C_삼각비", "relation_type": "REQUIRES"}, # Placeholder for high school concept
            {"from_concept_id": "C_순열과조합고", "to_concept_id": "C_경우의수", "relation_type": "REQUIRES"}, # Placeholder for high school concept

            # H-COMMON
            {"from_concept_id": "C_항등식과나머지정리", "to_concept_id": "C_다항식의연산", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_복소수", "to_concept_id": "C_제곱근", "relation_type": "REQUIRES"}, # Assuming C_제곱근 is a middle school concept
            {"from_concept_id": "C_이차함수와이차방정식의관계", "to_concept_id": "C_이차함수와그래프", "relation_type": "LINKS"},
            {"from_concept_id": "C_이차함수와이차방정식의관계", "to_concept_id": "C_이차방정식", "relation_type": "LINKS"},
            {"from_concept_id": "C_원의방정식", "to_concept_id": "C_피타고라스의정리", "relation_type": "LINKS"},
            {"from_concept_id": "C_원의방정식", "to_concept_id": "C_이차함수와그래프", "relation_type": "LINKS"},
            {"from_concept_id": "C_합성함수와역함수", "to_concept_id": "C_함수", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_순열", "to_concept_id": "C_경우의수", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_조합", "to_concept_id": "C_경우의수", "relation_type": "REQUIRES"},

            # MATH-I
            {"from_concept_id": "C_지수로그함수와그래프", "to_concept_id": "C_지수로그의정의와성질", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_지수로그함수와그래프", "to_concept_id": "C_거듭제곱근", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_삼각함수그래프", "to_concept_id": "C_일반각과호도법", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_사인법칙과코사인법칙", "to_concept_id": "C_삼각함수그래프", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_수학적귀납법", "to_concept_id": "C_등차등비수열", "relation_type": "REQUIRES"},

            # MATH-II
            {"from_concept_id": "C_미분계수", "to_concept_id": "C_함수의극한", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_도함수", "to_concept_id": "C_미분계수", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_함수의증가감소극대극소", "to_concept_id": "C_도함수", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_부정적분", "to_concept_id": "C_도함수", "relation_type": "REVERSE_OF"},
            {"from_concept_id": "C_정적분", "to_concept_id": "C_부정적분", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_정적분의활용", "to_concept_id": "C_정적분", "relation_type": "REQUIRES"},

            # CALC
            {"from_concept_id": "C_무한급수", "to_concept_id": "C_수열의극한", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_초월함수의미분", "to_concept_id": "C_도함수", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_초월함수의미분", "to_concept_id": "C_지수로그함수와그래프", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_초월함수의미분", "to_concept_id": "C_삼각함수그래프", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_치환적분법", "to_concept_id": "C_부정적분", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_부분적분법", "to_concept_id": "C_부정적분", "relation_type": "REQUIRES"},

            # PSTAT
            {"from_concept_id": "C_중복순열조합", "to_concept_id": "C_조합", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_조건부확률", "to_concept_id": "C_확률의기본성질", "relation_type": "REQUIRES"},

            # GEO
            {"from_concept_id": "C_이차곡선", "to_concept_id": "C_원의방정식", "relation_type": "REQUIRES"},
            {"from_concept_id": "C_벡터의내적", "to_concept_id": "C_벡터의연산", "relation_type": "REQUIRES"},
        ]
        for data in relations_data:
            db.add(ConceptRelation(**data))
        db.commit()

        print("Knowledge graph populated successfully!")
    except Exception as e:
        print(f"Error populating knowledge graph: {e}")
        db.rollback()
    finally:
        db.close()

    # --- V2 Knowledge Graph Expansion Placeholder ---
    # In V2, this section would contain logic to:
    # 1. Add new curriculums and concepts for advanced topics.
    # 2. Define more complex concept relations (e.g., cross-curriculum prerequisites).
    # 3. Potentially integrate with external data sources for automated graph enrichment.
    # Example:
    # new_concepts = [
    #     {"concept_id": "C_ADV_CALC_001", "curriculum_id": "CALC", "concept_name": "다변수 미적분", "description": "다변수 함수의 미분과 적분"},
    # ]
    # for data in new_concepts:
    #     db.add(ConceptsLibrary(**data))
    # db.commit()
    #
    # new_relations = [
    #     {"from_concept_id": "C_ADV_CALC_001", "to_concept_id": "C_초월함수의미분", "relation_type": "REQUIRES"},
    # ]
    # for data in new_relations:
    #     db.add(ConceptRelation(**data))
    # db.commit()
    # ------------------------------------------------

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) # Ensure tables are created
    db_session = next(get_db())
    populate_knowledge_graph(db_session)
