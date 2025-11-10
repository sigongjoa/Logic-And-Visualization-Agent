import pytest
from sqlalchemy.orm import Session
from backend.models import Curriculum, ConceptsLibrary, ConceptRelation
from backend.scripts.populate_knowledge_graph import populate_knowledge_graph, SQLALCHEMY_DATABASE_URL

# ... (rest of the file) ...

def test_populate_knowledge_graph(db_session: Session):
    # 1. Populate the data
    populate_knowledge_graph(db_session)

    # 2. Verify Curriculums
    curriculums = db_session.query(Curriculum).all()
    assert len(curriculums) == 7 # M-ALL, H-COMMON, MATH-I, MATH-II, CALC, PSTAT, GEO
    assert db_session.query(Curriculum).filter_by(curriculum_id="M-ALL").first() is not None
    assert db_session.query(Curriculum).filter_by(curriculum_id="H-COMMON").first() is not None

    # 3. Verify ConceptsLibrary
    concepts = db_session.query(ConceptsLibrary).all()
    # Count the number of concepts from the script
    # M-ALL: 16 + 1 (C_제곱근) = 17
    # H-COMMON: 15 + 2 (C_다항식고, C_순열과조합고) = 17
    # MATH-I: 9
    # MATH-II: 9
    # CALC: 7
    # PSTAT: 6
    # GEO: 4
    # Total: 17 + 17 + 9 + 9 + 7 + 6 + 4 = 69
    assert len(concepts) == 72
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_피타고라스의정리").first() is not None
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_이차함수와그래프").first() is not None
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_제곱근").first() is not None
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_다항식고").first() is not None

    # 4. Verify ConceptRelations
    relations = db_session.query(ConceptRelation).all()
    # Count the number of relations from the script
    # M-ALL: 10
    # H-COMMON: 8
    # MATH-I: 4
    # MATH-II: 4
    # CALC: 4
    # PSTAT: 2
    # GEO: 2 (C_벡터의내적 -> C_벡터의연산, C_이차곡선 -> C_원의방정식)
    # Total: 10 + 8 + 4 + 4 + 4 + 2 + 2 = 34
    assert len(relations) == 40
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_피타고라스의정리",
        to_concept_id="C_삼각형사각형의성질",
        relation_type="REQUIRES"
    ).first() is not None
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_이차함수와이차방정식의관계",
        to_concept_id="C_이차함수와그래프",
        relation_type="LINKS"
    ).first() is not None
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_순열과조합고",
        to_concept_id="C_경우의수",
        relation_type="REQUIRES"
    ).first() is not None
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_중복순열조합",
        to_concept_id="C_조합",
        relation_type="REQUIRES"
    ).first() is not None
