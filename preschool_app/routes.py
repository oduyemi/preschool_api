from datetime import timedelta, datetime
from fastapi import APIRouter, Request, status, Depends, HTTPException
from sqlalchemy.orm import Session
from preschool_app import starter, models, schemas
from preschool_app.dependencies import get_db
from preschool_app.authourize import decode_token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List
from preschool_app.models import Program, Class, Student, Admission, Role, Staff

preschool_router = APIRouter()



#     --   G E T   R E Q U E S T S   --

@starter.get("/")
async def get_index():
    return {"message": "Welcome to Preschool API"}

@starter.get("/programs", response_model=List[schemas.ProgramResponse])
async def get_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    return programs

@starter.get("/program/id", response_model = schemas.ProgramResponse)
async def get_program(id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not available!")
    return program

@starter.get("/classes", response_model=List[schemas.ClassResponse])
async def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    return classes

@starter.get("/class/id", response_model = schemas.ClassResponse)
async def get_class(ID: int, db: Session = Depends(get_db)):
    student_class = db.query(Class).filter(Class.id == class_id).first()
    if student_class is None:
        raise HTTPException(status_code=404, detail="Class not available!")
    return student_class

@starter.get("/students", response_model=List[schemas.StudentResponse])
async def get_students():
    students = db.query(Student).all()
    return students

@starter.get("/student/student_id", response_model=List[schemas.StudentResponse])
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not available!")
    return student

@starter.get("/departments", response_model=List[schemas.DepartmentResponse])
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return departments

@starter.get("/department/id", response_model = schemas.DepartmentResponse)
async def get_departments(id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == id).first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not available!")
    return department

@starter.get("/roles", response_model=List[schemas.RoleResponse])
async def get_departments(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    result = []
    for role in roles:
        staff_data = db.query(Staff).filter(Staff.role_id == role.id).all()
        role_info = {
            "id": role.id,
            "name": role.name,
            "staff": [{"id": staff.id, "name": staff.name} for staff in staff_data]
            }
        result.append(role_info)
    if not result:
        return roles
    return result














#     --   C R E A T E   R E Q U E S T S   --

@starter.post("/admission", response_model = schemas.AdmissionResponse)
async def create_admission(student_id: int, program_id: int):
    new_admission = Admission(student_id=student_id, program_id=program_id)
    new_admission.generate_student_number()

    if student_id and program_id:
        session.add(new_admission)
        session.commit()
        return new_admission
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/programs", response_model=schemas.ProgramRequest)
async def create_program(Name: str, Description:str, db: Session = Depends(get_db)):
    db_program = models.Program(name=Name, description=Description)
    if Name and Description:
        db.add(db_program)
        db.commit()
        db.refresh(db_program)
        return db_program
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/class", response_model=schemas.ClassRequest)
async def create_class(Name: str, db: Session = Depends(get_db)):
    db_class = models.Class(name = Name)
    if Name:
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        return db_class
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/department", response_model=schemas.DepartmentRequest)
async def create_department(Name: str, db: Session = Depends(get_db)):
    db_department = models.Department(name = Name)
    if Name:
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/role", response_model=schemas.RoleRequest)
async def create_role(Name: str, db: Session = Depends(get_db)):
    staff_id = None
    db_role = models.Role(name = Name)
    if Name:
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/gender", response_model=schemas.GenderRequest)
async def create_gender(Name: str, db: Session = Depends(get_db)):
    db_gender = models.Gender(name = Name)
    if Name:
        db.add(db_gender)
        db.commit()
        db.refresh(db_gender)
        return db_gender
    else:
        raise HTTPException(status_code=400, detail="Invalid input")


#     --   U P D A T E   R E Q U E S T S   --