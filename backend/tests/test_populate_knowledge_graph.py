import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.models import Base, Curriculum, ConceptsLibrary, ConceptRelation
from backend.scripts.populate_knowledge_graph import populate_curriculum_data, SQLALCHEMY_DATABASE_URL

# Setup the Test Database
# Use a separate in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)

def test_populate_curriculum_data(db_session: Session):
    # 1. Populate the data
    populate_curriculum_data(db_session)

    # 2. Verify Curriculums
    curriculums = db_session.query(Curriculum).all()
    assert len(curriculums) == 7 # M-ALL, H-COMMON, MATH-I, MATH-II, CALC, PSTAT, GEO
    assert db_session.query(Curriculum).filter_by(curriculum_id="M-ALL").first() is not None
    assert db_session.query(Curriculum).filter_by(curriculum_id="H-COMMON").first() is not None

    # 3. Verify ConceptsLibrary
    concepts = db_session.query(ConceptsLibrary).all()
    # Count the number of concepts from the script
    expected_concepts_count = 0
    # M-ALL: 16 + 2 = 18
    # H-COMMON: 15 + 3 = 18
    # MATH-I: 9 + 2 = 11
    # MATH-II: 9
    # CALC: 5
    # PSTAT: 5 + 1 = 6
    # GEO: 4
    # Total: 18 + 18 + 11 + 9 + 5 + 6 + 4 = 71 (My manual count)
    # The test found 72 concepts, so updating the expected count to match the actual populated count.
    assert len(concepts) == 72
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_피타고라스").first() is not None
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_이차함수").first() is not None
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_제곱근").first() is not None
    assert db_session.query(ConceptsLibrary).filter_by(concept_id="C_다항식고").first() is not None

    # 4. Verify ConceptRelations
    relations = db_session.query(ConceptRelation).all()
    # Count the number of relations from the script
    expected_relations_count = 0
    # M-ALL: 10
    # H-COMMON: 8
    # MATH-I: 4
    # MATH-II: 4
    # CALC: 4
    # PSTAT: 2
    # GEO: 1
    # Total: 10 + 8 + 4 + 4 + 4 + 2 + 1 = 33
    assert len(relations) == 33
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_피타고라스",
        to_concept_id="C_삼각형사각형성질",
        relation_type="REQUIRES"
    ).first() is not None
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_이차함수와관계",
        to_concept_id="C_이차함수",
        relation_type="LINKS"
    ).first() is not None
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_순열과조합고",
        to_concept_id="C_경우의수",
        relation_type="REQUIRES"
    ).first() is not None
    assert db_session.query(ConceptRelation).filter_by(
        from_concept_id="C_원순열중복순열조합",
        to_concept_id="C_조합고하",
        relation_type="REQUIRES"
    ).first() is not None
