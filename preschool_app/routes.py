from fastapi import APIRouter, Request, status
from sqlalchemy.orm import Session
from preschool_app import starter
from .models import Student


router = APIRouter()

students = []

@router.get("/")
async def get_index():
    return{"message": "Welcome to Preschool API"}

@starter.get("/students")
def get_students():
    pass 
    return {"message": "students data"}















