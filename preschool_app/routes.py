from datetime import timedelta, datetime
from fastapi import APIRouter, Request, status, Depends, HTTPException, Form
from sqlalchemy.orm import Session, joinedload
from preschool_app import starter, models, schemas
from preschool_app.dependencies import get_db, get_current_user
from preschool_app.authorize import decode_token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List
from preschool_app.models import Program, Class, Student, Admission, Role, Staff, Department
from sqlalchemy import func

preschool_router = APIRouter()


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')





#     --   G E T   R E Q U E S T S   --

@starter.get("/")
async def get_index():
    return {"message": "Welcome to Preschool API"}

@starter.get("/about")
async def get_index():
    return {"message": "Welcome to our About page! We are here to provide valuable information."}

@starter.get("/contact")
async def get_index():
    return {"message": "Got questions or concerns? Feel free to contact us! Email: support@storytimepreschool.com"}

@starter.get("/programs", response_model=List[schemas.ProgramResponse])
async def get_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    if not programs:
        raise HTTPException(status_code=404, detail="Programs not available!")
    return programs

@starter.get("/programs/program_id", response_model = schemas.ProgramResponse)
async def get_program_by_id(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
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



@starter.get("/classes/class_id", response_model=schemas.ClassResponse)
async def get_class_by_id(class_id: int, db: Session = Depends(get_db)):
    student_class = db.query(Class).filter(Class.id == class_id).first()
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

@starter.get("/students/student_id", response_model=List[schemas.StudentResponse])
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
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


@starter.get("/staff/members/staff_id", response_model=schemas.StaffResponse)
async def get_staff_member_by_id(staff_id: int, db: Session = Depends(get_db)):
    staff_member = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff not available!")
    return staff_member

def convert_department_to_response(department):
    return [
        schemas.DepartmentResponse(id=dept.id, name=dept.name, staff_members=len(dept.staff_members))
        for dept in department
    ]

@starter.get("/departments", response_model=List[schemas.DepartmentResponse])
async def get_departments(db: Session = Depends(get_db)):
    department = db.query(Department).all()
    if not department:
        raise HTTPException(status_code=404, detail="Departments not available!")

    department_response_list = convert_department_to_response(department)

    return department_response_list


@starter.get("/departments/department_id", response_model = schemas.DepartmentResponse)
async def get_department_by_id(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
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

@starter.get("/roles/role_id", response_model=List[schemas.RoleResponse])
async def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()  
    if not role:
        raise HTTPException(status_code=404, detail="Role not available!")
    result = []
    staff_data = db.query(Staff).filter(Staff.role_id == role.id).all()
    role_info = {
        "id": role.id,
        "name": role.name,
        "staff": [staff.name for staff in staff_data]
    }
    result.append(role_info)
    return result



@starter.get("/medical/categories", response_model=List[schemas.MedicalCategoryResponse])
async def get_medical_categories(db: Session = Depends(get_db)):
    categories = db.query(models.MedicalCategory).all()
    return categories

@starter.get("/medical/category/{category_id}", response_model=List[schemas.MedicalConditionResponse])
async def get_conditions_by_category(category_id: int, db: Session = Depends(get_db)):
    conditions = db.query(models.MedicalCondition).filter(models.MedicalCondition.medical_category_id == category_id).all()
    return conditions


@starter.get("/medical/{medical_id}", response_model=schemas.MedicalConditionResponse)
async def get_medical_condition_by_id(medical_id: int, db: Session = Depends(get_db)):
    medical_condition = db.query(models.MedicalCondition).filter(models.MedicalCondition.id == medical_id).first()
    if not medical_condition:
        raise HTTPException(status_code=404, detail="Medical condition not found")
    return medical_condition

@starter.get("/student/{student_id}/medical-conditions", response_model=List[schemas.MedicalConditionResponse])
async def get_student_medical_conditions(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.medical_conditions


@starter.get("/daily-activities", response_model=List[schemas.DailyActivityResponse])
async def get_daily_activities(
    student_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    query = session.query(DailyActivity).filter(DailyActivity.student_id == student_id)

    if start_date:
        query = query.filter(DailyActivity.date >= start_date)
    if end_date:
        query = query.filter(DailyActivity.date <= end_date)

    activities = query.all()

    if not activities:
        raise HTTPException(status_code=404, detail="No daily activities found")

    return activities




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


@starter.post("/program", response_model=schemas.ProgramRequest)
async def create_new_program(Name: str, Description:str, db: Session = Depends(get_db)):
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
async def create_new_class(Name: str, program_id: int, db: Session = Depends(get_db)):
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



@starter.post("/gender", response_model=schemas.GenderRequest)
async def create_new_gender(Name: str, db: Session = Depends(get_db)):
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


@starter.post("/attendance", response_model=schemas.AttendanceResponse)
async def mark_attendance(attendance_data: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == attendance_data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    total_students = db.query(models.Student).count()
    if total_students == 0:
        raise HTTPException(status_code=404, detail="There are no students at the moment")

    new_attendance = models.Attendance(student_id=student_id, status=status)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


@starter.post("/student/{student_id}/medical-condition/{condition_id}", response_model=schemas.StudentMedicalConditionAssociationResponse)
async def associate_medical_condition(student_id: int, condition_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    condition = db.query(models.MedicalCondition).filter(models.MedicalCondition.id == condition_id).first()
    if not condition:
        raise HTTPException(status_code=404, detail="Medical condition not found")

    association = models.StudentMedicalConditionAssociation(student_id=student_id, medical_condition_id=condition_id)
    db.add(association)
    db.commit()
    db.refresh(association)

    return association






        #  - - Staff
staff_router = APIRouter()

def get_current_user_role(current_user: schemas.StaffResponse = Depends(get_current_user)):
    return current_user.role


#     --   G E T   R E Q U E S T S   --
@starter.get("/staff/schedule/{staff_id}", response_model=schemas.ScheduleResponse)
async def get_staff_schedule(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff.schedule



    #     --   P O S T   R E Q U E S T S   --


@staff_router.post("/staff/register", response_model=schemas.StaffCreate)
async def register_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    existing_staff = db.query(models.Staff).filter(models.Staff.email == staff_data.email).first()
    if existing_staff:
        raise HTTPException(status_code=400, detail="Staff with this email already registered")

    new_staff = models.Staff(**staff_data.dict())
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    return new_staff

@staff_router.post("/staff/login", response_model=schemas.Token)
async def login_staff(staff_data: schemas.StaffLogin, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.email == staff_data.email).first()
    if not staff or not staff.verify_password(staff_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": staff.email, "role": staff.role})

    return {"access_token": access_token, "token_type": "bearer"}

@staff_router.post("/schedule", response_model=schemas.ScheduleResponse)
async def create_staff_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@staff_router.post("/department", response_model=schemas.DepartmentRequest)
async def create_new_department(Name: str, db: Session = Depends(get_db)):
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

@staff_router.post("/role", response_model=schemas.RoleRequest)
async def create_new_role(Name: str, db: Session = Depends(get_db)):
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

@staff_router.post("/daily-activities", response_model=schemas.DailyActivityResponse)
async def add_daily_activity(
    activity_data: schemas.DailyActivityRequest,
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can add daily activities.")

    student = session.query(Student).filter(Student.id == activity_data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    new_activity = DailyActivity(**activity_data.dict())
    session.add(new_activity)
    session.commit()
    session.refresh(new_activity)

    return new_activity

# ...

@staff_router.post("/billing", response_model=schemas.BillingResponse)
async def create_bill(
    student_id: int, amount: float, due_date: datetime,
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role != "accountant":
        raise HTTPException(status_code=403, detail="Only accountants can create bills.")

    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    new_bill = Billing(student_id=student_id, amount=amount, due_date=due_date)
    session.add(new_bill)
    session.commit()
    session.refresh(new_bill)

    return new_bill

# ...

@staff_router.post("/payment", response_model=schemas.PaymentResponse)
async def record_payment(
    bill_id: int, amount_paid: float, payment_method: str,
    current_user_role: str = Depends(get_current_user_role)
):
    if current_user_role != "accountant":
        raise HTTPException(status_code=403, detail="Only accountants can record payments.")

    bill = session.query(Billing).filter(Billing.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    if amount_paid > bill.amount:
        raise HTTPException(status_code=400, detail="Amount paid exceeds the billed amount")

    new_payment = Payment(bill_id=bill_id, amount_paid=amount_paid, payment_method=payment_method)
    session.add(new_payment)
    session.commit()
    session.refresh(new_payment)

    if amount_paid == bill.amount:
        bill.status = "paid"
    elif amount_paid < bill.amount:
        bill.status = "partial"

    session.commit()
    session.refresh(bill)

    return new_payment



#     --   U P D A T E   R E Q U E S T S   --

@staff_router.put("/programs/program_id", response_model=schemas.ProgramRequest)
async def edit_program(
    name: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    program_check = db.query(Program).filter(Program.name == name).first()
    if not program_check:
        raise HTTPException(status_code=404, detail=f"Program does not exist")

    if name is not None:
        program_check.name = name

    if description is not None:
        program_check.description = description

    db.commit()
    db.refresh(program_check)

    return program_check


@staff_router.put("/staff_members/staff_id", response_model=schemas.StaffRequest)
async def edit_staff(
    email: str = Form,
    name: str = Form,
    address: str = Form,
    phone: str = Form,
    password: str = Form,
    department: int = Form,
    role: str = Form,
    image: str = Form,
    current_user: schemas.StaffResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    staff_check = db.query(Staff).filter(Staff.email == email).first()
    if not staff_check:
        raise HTTPException(status_code=404, detail=f"Staff does not exist")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have the permission to make this edit")

    if name is not None:
        staff_check.name = name

    if phone is not None:
        staff_check.phone = phone

    if password is not None:
        staff_check.password = hash_password_function(password)

    if address is not None:
        staff_check.address = address

    if role is not None:
        staff_check.role = role

    if image is not None:
        staff_check.image = image

    db.commit()
    db.refresh(staff_check)

    return staff_check



#      --   D E L E T E   R E Q U E S T S   --

def delete_entity_by_id(entity_type, entity_id, current_user, db):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail=f"You do not have the permission to delete {entity_type}")

    current_entity = db.query(entity_type).filter(entity_type.id == entity_id).first()
    if not current_entity:
        raise HTTPException(status_code=404, detail=f"{entity_type} with ID {entity_id} not available")

    db.delete(current_entity)
    db.commit()

    return current_entity

@staff_router.delete("/staff/id", response_model=schemas.StaffRequest)
async def delete_staff(staff_id: int, current_user: schemas.StaffResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_entity_by_id(models.Staff, staff_id, current_user, db)

@staff_router.delete("/program/id", response_model=schemas.ProgramRequest)
async def delete_program(program_id: int, current_user: schemas.StaffResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_entity_by_id(models.Program, program_id, current_user, db)

@staff_router.delete("/class/id", response_model=schemas.ClassRequest)
async def delete_class(class_id: int, current_user: schemas.StaffResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_entity_by_id(models.Class, class_id, current_user, db)

@staff_router.delete("/student/id", response_model=schemas.StudentRequest)
async def delete_student(student_id: int, current_user: schemas.StaffResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_entity_by_id(models.Student, student_id, current_user, db)

@staff_router.delete("/daily-activities/{activity_id}", response_model=schemas.DailyActivityResponse)
async def delete_daily_activity(activity_id: int):
    activity = session.query(DailyActivity).filter(DailyActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Daily activity not found")

    session.delete(activity)
    session.commit()

    return activity




       #  - - Parent
parent_router = APIRouter()

#      --   G E T   R E Q U E S T S   --
@starter.get("/parents", response_model=schemas.ParentResponse)
async def get_parent_by_id(db: Session = Depends(get_db)):
    parents = db.query(models.Parent).all()
    if not parents:
        raise HTTPException(status_code=404, detail="Parents not found")
    return parents

@starter.get("/parents/{parent_id}", response_model=schemas.ParentResponse)
async def get_parent_by_id(parent_id: int, db: Session = Depends(get_db)):
    parent = db.query(models.Parent).filter(models.Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent



#      --   P O S T   R E Q U E S T S   --

@parent_router.post("/parent/register", response_model=schemas.ParentCreate)
async def register_parent(parent_data: schemas.ParentCreate, db: Session = Depends(get_db)):
    existing_parent = db.query(models.Parent).filter(models.Parent.email == parent_data.email).first()
    if existing_parent:
        raise HTTPException(status_code=400, detail="Parent with this email already registered")

    new_parent = models.Parent(**parent_data.dict())
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)

    return new_parent

@parent_router.post("/parent/login", response_model=schemas.Token)
async def parent_login(parent_login: schemas.ParentLogin, db: Session = Depends(get_db)):
    parent = db.query(models.Parent).filter(models.Parent.email == parent_data.email).first()
    if not parent or not parent.verify_password(parent_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": parent.email, "role": "parent"})

    return {"access_token": access_token, "token_type": "bearer"}


