from datetime import timedelta, datetime
from fastapi import APIRouter, Request, status, Depends, HTTPException
from sqlalchemy.orm import Session
from preschool_app import starter
from .authourize import create_access_token, decode_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional


router = APIRouter()

def authenticate_user(username: str, password: str) -> Optional[dict]:

    users_db = {
        "user1": {"username": "user1", "password": "password1"},
        "user2": {"username": "user2", "password": "password2"},
    }

    user = users_db.get(username)
    if user and user["password"] == password:
        return {"sub": username}

    return None

@starter.get("/")
async def get_index():
    return{"message": "Welcome to Preschool API"}

@starter.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@starter.get("/secure-data")
async def secure_data(current_user: dict = Depends(decode_token)):
    return {"message": "This is secure data!", "current_user": current_user}




















