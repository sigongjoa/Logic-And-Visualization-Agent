from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pacer.backend import models

# Database setup
# Using a file-based SQLite DB for local development.
# The production environment would use PostgreSQL or MySQL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./atlas.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project: ATLAS - AI Coaching Platform API (V1)",
    description="학생의 4축 잠재 공간 모델을 기반으로 코칭 활동을 지원하는 통합 API",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Project: ATLAS API"}

from pacer.backend.routers import assessments, submissions
app.include_router(assessments.router)
app.include_router(submissions.router)
