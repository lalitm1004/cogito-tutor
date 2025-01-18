from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.background import BackgroundTasks
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from sqlalchemy import create_engine, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime, timedelta, date
from typing import Optional, Dict, List
import httpx
import jwt
import json
import os
import uuid
import random
from dotenv import load_dotenv
from generation_methods.completions import Completions

# FastAPI app initialization
app = FastAPI()

load_dotenv()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Database configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OAuth2 scopes
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/tasks"
]


# Database Models
class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    avatar_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship
    courses = relationship("Courses", backref="user")


class UserTokens(Base):
    __tablename__ = "user_tokens"

    user_id = Column(String, primary_key=True)
    google_tokens = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Courses(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    topic = Column(String, nullable=False)
    img_id = Column(String, nullable=False)
    schedule = Column(JSONB)
    day_1_flashcards = Column(JSONB, nullable=True)
    day_1_quiz = Column(JSONB, nullable=True)
    day_2_flashcards = Column(JSONB, nullable=True)
    day_2_quiz = Column(JSONB, nullable=True)
    day_3_flashcards = Column(JSONB, nullable=True)
    day_3_quiz = Column(JSONB, nullable=True)
    day_4_flashcards = Column(JSONB, nullable=True)
    day_4_quiz = Column(JSONB, nullable=True)
    day_5_flashcards = Column(JSONB, nullable=True)
    day_5_quiz = Column(JSONB, nullable=True)
    day_6_flashcards = Column(JSONB, nullable=True)
    day_6_quiz = Column(JSONB, nullable=True)
    day_7_flashcards = Column(JSONB, nullable=True)
    day_7_quiz = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Create database tables
Base.metadata.create_all(bind=engine)


# Pydantic Models
class TaskCreate(BaseModel):
    title: str
    due_date: date


class CourseCreate(BaseModel):
    topic: str
    description: str


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User Management
class UserManager:
    @staticmethod
    async def create_or_update_user(db: Session, user_data: dict) -> Users:
        user = db.query(Users).filter(Users.id == user_data['id']).first()

        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.updated_at = datetime.utcnow()
        else:
            user = Users(**user_data)
            db.add(user)

        db.commit()
        db.refresh(user)
        return user


# Token Management
class TokenManager:
    @staticmethod
    async def store_tokens(db: Session, user_id: str, tokens: dict):
        db_tokens = db.query(UserTokens).filter(UserTokens.user_id == user_id).first()

        if db_tokens:
            db_tokens.google_tokens = json.dumps(tokens)
            db_tokens.updated_at = datetime.utcnow()
        else:
            db_tokens = UserTokens(
                user_id=user_id,
                google_tokens=json.dumps(tokens)
            )
            db.add(db_tokens)

        db.commit()

    @staticmethod
    async def get_valid_tokens(db: Session, user_id: str) -> Optional[dict]:
        db_tokens = db.query(UserTokens).filter(UserTokens.user_id == user_id).first()

        if not db_tokens:
            return None

        tokens = json.loads(db_tokens.google_tokens)
        expires_at = datetime.fromisoformat(tokens['expires_at'])

        if expires_at <= datetime.utcnow() + timedelta(minutes=5):
            try:
                new_tokens = await TokenManager._refresh_token(tokens['refresh_token'])
                tokens.update({
                    'access_token': new_tokens['access_token'],
                    'expires_at': (datetime.utcnow() +
                                   timedelta(seconds=new_tokens['expires_in'])).isoformat()
                })
                await TokenManager.store_tokens(db, user_id, tokens)
            except Exception as e:
                return None

        return tokens

    @staticmethod
    async def _refresh_token(refresh_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'client_id': GOOGLE_CLIENT_ID,
                    'client_secret': GOOGLE_CLIENT_SECRET,
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token',
                }
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Token refresh failed")
            return response.json()

    @staticmethod
    def create_access_token(user_id: str) -> str:
        expiration = datetime.utcnow() + timedelta(days=1)
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': expiration
            },
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

    @staticmethod
    async def revoke_tokens(db: Session, user_id: str):
        db.query(UserTokens).filter(UserTokens.user_id == user_id).delete()
        db.commit()


# Course Management
async def generate_day_materials(db: Session, course_id: str, day_number: int):
    try:
        course = db.query(Courses).filter(Courses.id == course_id).first()
        if not course:
            return

        day_schedule = course.schedule[f'day_{day_number}']
        subtopic = day_schedule['subtopic']

        # Generate flashcards for the day's subtopic
        flashcards = Completions.return_flashcards(subtopic)
        # Generate quiz for the day's subtopic (medium difficulty)
        quiz = Completions.return_quiz(subtopic, difficulty=2)

        # Update the course with the generated materials
        setattr(course, f'day_{day_number}_flashcards', flashcards)
        setattr(course, f'day_{day_number}_quiz', quiz)

        db.commit()
    except Exception as e:
        print(f"Error generating materials for day {day_number}: {str(e)}")
        db.rollback()


# Authentication Dependency
async def get_current_user(authorization: str = Header(...)) -> str:
    try:
        token = authorization.replace('Bearer ', '')
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Routes
@app.get("/login")
async def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return JSONResponse({
        "auth_url": authorization_url,
        "state": state
    })


@app.get("/callback")
async def callback(code: str, state: str, db: Session = Depends(get_db)):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(code=code)

    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        requests.Request(),
        GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=10
    )

    user_data = {
        'id': id_info['sub'],
        'email': id_info['email'],
        'first_name': id_info.get('given_name', ''),
        'last_name': id_info.get('family_name', ''),
        'avatar_url': id_info.get('picture', '')
    }

    await UserManager.create_or_update_user(db, user_data)

    tokens = {
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token': credentials.id_token,
        'expires_at': (datetime.utcnow() +
                       timedelta(seconds=credentials.expiry.timestamp() -
                                         datetime.utcnow().timestamp())).isoformat()
    }

    await TokenManager.store_tokens(db, user_data['id'], tokens)
    jwt_token = TokenManager.create_access_token(user_data['id'])

    redirect_url = f"{FRONTEND_URL}?token={jwt_token}"
    return RedirectResponse(url=redirect_url)


@app.get("/profile")
async def get_user_profile(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "avatar_url": user.avatar_url
    }


# Course list endpoint
@app.get("/tutor")
async def tutor(
        user_id: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        courses = db.query(Courses).filter(Courses.user_id == user_id).all()
        if not courses:
            return JSONResponse({"courses": None})

        course_list = [{
            "id": course.id,
            "topic": course.topic,
            "img_id": course.img_id
        } for course in courses]

        return JSONResponse({"courses": course_list})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Course creation endpoint
@app.post("/new")
async def create_course(
        course: CourseCreate,
        user_id: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Check if user has reached course limit
    user_courses = db.query(Courses).filter(Courses.user_id == user_id).all()
    if len(user_courses) >= 3:
        raise HTTPException(
            status_code=400,
            detail="Maximum number of courses (3) reached"
        )

    try:
        # Generate course schedule
        schedule = Completions.return_week_schedule(course.topic, course.description)

        # Generate random image ID between 1-99
        img_id = str(random.randint(1, 99)).zfill(2)

        # Create new course
        new_course = Courses(
            id=str(uuid.uuid4()),
            user_id=user_id,
            topic=course.topic,
            img_id=img_id,
            schedule=schedule
        )

        db.add(new_course)
        db.commit()
        db.refresh(new_course)

        return JSONResponse({
            "message": "Course created successfully",
            "course": {
                "id": new_course.id,
                "topic": new_course.topic,
                "img_id": new_course.img_id
            }
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Day content generation endpoint
# Request body model_docs
class DayContentRequest(BaseModel):
    course_id: str
    day_number: int

@app.post("/generate-day-content")
async def get_or_generate_day_content(
    request: DayContentRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate day number
    if not 1 <= request.day_number <= 7:
        raise HTTPException(
            status_code=400,
            detail="Day number must be between 1 and 7"
        )

    # Get user's courses
    user_courses = db.query(Courses).filter(Courses.user_id == user_id).all()
    user_course_ids = [course.id for course in user_courses]

    # Check if the course exists and belongs to the user
    if request.course_id not in user_course_ids:
        raise HTTPException(
            status_code=404,
            detail="Course not found or not authorized to access this course"
        )

    # Get the course
    course = db.query(Courses).filter(Courses.id == request.course_id).first()

    # Check if content already exists for this day
    flashcards = getattr(course, f'day_{request.day_number}_flashcards')
    quiz = getattr(course, f'day_{request.day_number}_quiz')

    if flashcards and quiz:
        # Return existing content
        return {
            "flashcards": flashcards,
            "quiz": quiz
        }

    try:
        # Get the day's subtopic from schedule
        day_schedule = course.schedule[f'day_{request.day_number}']
        subtopic = day_schedule['subtopic']

        # Generate new content
        flashcards = Completions.return_flashcards(subtopic)
        quiz = Completions.return_quiz(subtopic, difficulty=2)

        # Update the course with the generated materials
        setattr(course, f'day_{request.day_number}_flashcards', flashcards)
        setattr(course, f'day_{request.day_number}_quiz', quiz)

        db.commit()

        return {
            "flashcards": flashcards,
            "quiz": quiz
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating content for day {request.day_number}: {str(e)}"
        )

# Request body model for schedule
class CourseScheduleRequest(BaseModel):
    course_id: str

@app.post("/get-schedule")
async def get_course_schedule(
    request: CourseScheduleRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's courses
    user_courses = db.query(Courses).filter(Courses.user_id == user_id).all()
    user_course_ids = [course.id for course in user_courses]

    # Check if the course exists and belongs to the user
    if request.course_id not in user_course_ids:
        raise HTTPException(
            status_code=404,
            detail="Course not found or not authorized to access this course"
        )

    # Get the course
    course = db.query(Courses).filter(Courses.id == request.course_id).first()

    return {
        "topic": course.topic,
        "schedule": course.schedule
    }


@app.post("/logout")
async def logout(
        user_id: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    await TokenManager.revoke_tokens(db, user_id)
    return JSONResponse({"message": "Logged out successfully"})

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)