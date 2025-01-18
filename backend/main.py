from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta, date
from typing import Optional, Dict
import httpx
import jwt
import json
import os
from dotenv import load_dotenv

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

    id = Column(String, primary_key=True)  # This will be the Google sub/user_id
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    avatar_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserTokens(Base):
    __tablename__ = "user_tokens"

    user_id = Column(String, primary_key=True)
    google_tokens = Column(JSONB)  # Stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Create database tables
Base.metadata.create_all(bind=engine)


# Pydantic Models
class TaskCreate(BaseModel):
    title: str
    due_date: date


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
            # Update existing user
            for key, value in user_data.items():
                setattr(user, key, value)
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
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


# Task Management
class TaskManager:
    @staticmethod
    async def get_default_task_list(access_token: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://tasks.googleapis.com/tasks/v1/users/@me/lists',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code,
                                    detail="Failed to get task lists")

            task_lists = response.json().get('items', [])
            if not task_lists:
                raise HTTPException(status_code=404, detail="No task list found")

            return task_lists[0]['id']

    @staticmethod
    async def create_task(access_token: str, task_list_id: str, title: str, due_date: date) -> dict:
        task_data = {
            'title': title,
            'due': f"{due_date}T00:00:00.000Z"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'https://tasks.googleapis.com/tasks/v1/lists/{task_list_id}/tasks',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                },
                json=task_data
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code,
                                    detail="Failed to create task")

            return response.json()


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

    # Add clock_skew_in_seconds parameter for token verification
    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        requests.Request(),
        GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=10  # Allow 10 seconds of clock skew
    )

    # Rest of your callback function remains the same
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


# Add a route to get user profile
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


@app.post("/tasks")
async def create_task(
        task: TaskCreate,
        user_id: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    tokens = await TokenManager.get_valid_tokens(db, user_id)
    if not tokens:
        raise HTTPException(status_code=401, detail="Google tokens not found")

    try:
        task_list_id = await TaskManager.get_default_task_list(tokens['access_token'])
        created_task = await TaskManager.create_task(
            tokens['access_token'],
            task_list_id,
            task.title,
            task.due_date
        )
        return JSONResponse({
            "message": "Task created successfully",
            "task": created_task
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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