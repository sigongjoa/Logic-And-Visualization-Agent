from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # New import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models

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

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:5173", # Frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

from .routers import anki_cards, assessments, coach_memos, coaches, llm_logs, reports, students, submissions, auth, notifications, users
app.include_router(assessments.router)
app.include_router(submissions.router)
app.include_router(auth.router)
app.include_router(notifications.router)
app.include_router(users.router)
app.include_router(reports.router)
app.include_router(students.router)
app.include_router(coach_memos.router)
app.include_router(llm_logs.router)
app.include_router(coaches.router) # Added coaches router
app.include_router(anki_cards.router) # Added anki_cards router
