from datetime import timedelta, datetime
from fastapi import APIRouter, Request, status, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from preschool_app import starter, models, schemas
from preschool_app.dependencies import get_db
from preschool_app.authourize import decode_token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List
from preschool_app.models import Program, Class, Student, Admission, Role, Staff, Department
from sqlalchemy import func

preschool_router = APIRouter()


#     --   G E T   R E Q U E S T S   --

@starter.get("/")
async def get_index():
    return {"message": "Welcome to Preschool API"}

@starter.get("/programs", response_model=List[schemas.ProgramResponse])
async def get_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    if not programs:
        raise HTTPException(status_code=404, detail="Programs not available!")
    return programs

@starter.get("/program/id", response_model = schemas.ProgramResponse)
async def get_program(id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not available!")
    return program

@starter.get("/classes", response_model=List[schemas.ClassResponse])
async def get_classes(db: Session = Depends(get_db)):
    classes = db.query(Class).options(joinedload(Class.program)).all()
    if not classes:
        raise HTTPException(status_code=404, detail="Classes not available!")
    result = []
    for class_deets in classes:
        program_data = db.query(Program).filter(Program.id == class_deets.program_id).all()
        class_info = {
            "id": class_deets.id,
            "name": class_deets.name, 
            "program": [program.name for program in program_data]
        }
        result.append(class_info)
    return result



@starter.get("/class/id", response_model=schemas.ClassResponse)
async def get_class(id: int, db: Session = Depends(get_db)):
    student_class = db.query(Class).filter(Class.id == id).first()
    if not student_class:
        raise HTTPException(status_code=404, detail="Class not available!")
    program_data = db.query(Program).filter(Program.id == student_class.program_id).all()
    class_info = {
        "id": student_class.id,
        "name": student_class.name,
        "program": [program.name for program in program_data],
    }
    return class_info

@starter.get("/students", response_model=List[schemas.StudentResponse])
async def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="Students not available!")
    return students

@starter.get("/student/student_id", response_model=List[schemas.StudentResponse])
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not available!")
    return student

@starter.get("/staff-members", response_model=List[schemas.StaffResponse])
async def get_staff_members(db: Session = Depends(get_db)):
    staff = db.query(Staff).all()
    if not staff :
        raise HTTPException(status_code=404, detail="Staff not available!")
    return staff


@starter.get("/staff/id", response_model=schemas.StaffResponse)
async def get_staff_member(id: int, db: Session = Depends(get_db)):
    member = db.query(Staff).all()
    if not member :
        raise HTTPException(status_code=404, detail="Staff member not available!")
    return member

@starter.get("/departments", response_model=List[schemas.StaffResponse])
async def get_departments(db: Session = Depends(get_db)):
    department = db.query(Department).all()
    if not department :
        raise HTTPException(status_code=404, detail="Departments not available!")
    return department

@starter.get("/department/id", response_model = schemas.DepartmentResponse)
async def get_department(id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not available!")
    return department

@starter.get("/roles", response_model=List[schemas.RoleResponse])
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()  
    if not roles:
        raise HTTPException(status_code=404, detail="Roles not available!")
    result = []
    for role in roles:
        staff_data = db.query(Staff).filter(Staff.role_id == role.id).all()
        role_info = {
            "id": role.id,
            "name": role.name,
            "staff": [staff.name for staff in staff_data]
        }
        result.append(role_info)
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
    available_program = db.query(models.Program).filter(func.lower(models.Program.name) == func.lower(Name)).first()
    if available_program:
        raise HTTPException(status_code=400, detail="This program already exists")
    db_program = models.Program(name=Name, description=Description)
    if Name and Description:
        db.add(db_program)
        db.commit()
        db.refresh(db_program)
        return db_program
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/class", response_model=schemas.ClassRequest)
async def create_class(Name: str, program_id: int, db: Session = Depends(get_db)):
    available_class = db.query(models.Class).filter(func.lower(models.Class.name) == func.lower(Name)).first()
    if available_class:
        raise HTTPException(status_code=400, detail="This class already exists")

    available_program = db.query(models.Program).filter(models.Program.id == program_id).first()
    if not available_program:
        raise HTTPException(status_code=400, detail="Program with this ID does not exist")

    db_class = models.Class(name = Name, program_id = program_id)
    if Name:
        db.add(db_class)
        db.commit()
        db.refresh(db_class)
        return db_class
    else:
        raise HTTPException(status_code=400, detail="Invalid input")

@starter.post("/department", response_model=schemas.DepartmentRequest)
async def create_department(Name: str, db: Session = Depends(get_db)):
    available_department = db.query(models.Department).filter(func.lower(models.Department.name) == func.lower(Name)).first()
    if available_department:
        raise HTTPException(status_code=400, detail="This department already exists")
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
    available_role = db.query(models.Role).filter(func.lower(models.Role.name) == func.lower(Name)).first()
    if available_role:
        raise HTTPException(status_code=400, detail="This role already exists")
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
    available_gender = db.query(models.Gender).filter(func.lower(models.Gender.name) == func.lower(Name)).first()
    if available_gender:
        raise HTTPException(status_code=400, detail="Gender already exists")
    db_gender = models.Gender(name = Name)
    if Name:
        db.add(db_gender)
        db.commit()
        db.refresh(db_gender)
        return db_gender
    else:
        raise HTTPException(status_code=400, detail="Invalid input")


#     --   U P D A T E   R E Q U E S T S   --