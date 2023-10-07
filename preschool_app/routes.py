from datetime import timedelta, datetime
from fastapi import APIRouter, Request, status, Depends, HTTPException
from sqlalchemy.orm import Session
from preschool_app import starter
from preschool_app.dependencies import get_db
from preschool_app.authourize import decode_token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from preschool_app.models import Program, Class, Student, Admission

preschool_router = APIRouter()



#     --   G E T   R E Q U E S T S   --

@starter.get("/")
async def get_index():
    return {"message": "Welcome to Preschool API"}

@starter.get("/programs")
async def get_programs():
    programs = db.query(Program).all()
    return programs

@starter.get("/program/program_id")
async def get_program(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not available!")
    return program

@starter.get("/classes")
async def get_classes():
    classes = db.query(Class).all()
    return classes

@starter.get("/class/class_id")
async def get_class():
    student_class = db.query(Class).filter(Class.id == class_id).first()
    if student_class is None:
        raise HTTPException(status_code=404, detail="Class not available!")
    return student_class

@starter.get("/students")
async def get_students():
    students = db.query(Student).all()
    return students

@starter.get("/student/student_id")
async def get_student():
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not available!")
    return student

#     --   G E T   R E Q U E S T S   --

@starter.post("/admission")
async def create_admission(student_id: int, program_id: int):
    new_admission = Admission(student_id=student_id, program_id=program_id)
    new_admission.generate_student_number()

    if student_id and program_id:
        session.add(new_admission)
        session.commit()
        return {"message": "Admission created successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid input")


