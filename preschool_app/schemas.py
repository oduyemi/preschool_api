from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Union


class Token(BaseModel):
    access_token: str
    token_type: str

class ProgramRequest(BaseModel):
    name: str
    description: str

class ProgramResponse(BaseModel):
    id: int
    name: str

class ClassRequest(BaseModel):
    name: str
    program_id: int
    class_teacher_id: Optional[int]
    assistant_teacher_id: Optional[int]

class ClassResponse(BaseModel):
    id: int
    name: str
    program: List[str]


class StudentRequest(BaseModel):
    name: str
    description: str
    age: int
    address: str
    gender_id: int
    class_id: int
    emergency_contact_id: int
    medical_condition_id: int
    is_disable: str
    image: str

class StudentResponse(BaseModel):
    id: int
    name: str
    description: str
    age: int
    address: str
    gender_id: int
    class_id: int
    emergency_contact_id: int
    medical_condition_id: int
    is_disable: str
    image: str


class AdmissionRequest(BaseModel):
    student_id: int
    program_id: int
    student_number: str
    date: datetime  

class AdmissionResponse(BaseModel):
    id: int
    student_id: int
    program_id: int
    student_number: str
    date: datetime  

class StaffRequest(BaseModel):
    name: str
    age: int
    gender_id: int
    address: str
    email: str
    phone: str
    password: str
    hashedpassword: str
    department: str
    role: str
    image: str

class StaffResponse(BaseModel):
    id: int
    name: str
    age: int
    gender_id: int
    address: str
    email: str
    phone: str
    password: str
    hashedpassword: str
    department: str
    role: str
    image: str

class DepartmentRequest(BaseModel):
    name: str
    staff_members: int

class DepartmentResponse(BaseModel):
    id: int
    name: str
    staff_members: int

class RoleRequest(BaseModel):
    name: str
    staff_id: Optional[int]

class RoleResponse(BaseModel):
    id: int
    name: str
    staff: List[Dict[str, Union[int, str]]]

class GenderRequest(BaseModel):
    name: str

class GenderResponse(BaseModel):
    id: int
    name: str

class AttendanceBase(BaseModel):
    date: Optional[datetime]
    status: str

class AttendanceCreate(AttendanceBase):
    student_id: int

class AttendanceResponse(AttendanceBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True

class ParentBase(BaseModel):
    name: str
    age: int
    gender_id: int
    address: str
    email: str
    phone: str

class ParentCreate(ParentBase):
    password: str

class ParentResponse(ParentBase):
    id: int

    class Config:
        orm_mode = True

class MedicalConditionBase(BaseModel):
    name: str

class MedicalConditionResponse(MedicalConditionBase):
    id: int

    class Config:
        orm_mode = True

class MedicalCategoryBase(BaseModel):
    name: str

class MedicalCategoryResponse(MedicalCategoryBase):
    id: int

    class Config:
        orm_mode = True

class MedicalConditionBase(BaseModel):
    name: str
    category_id: int

class MedicalConditionResponse(MedicalConditionBase):
    id: int
    category: MedicalCategoryResponse

    class Config:
        orm_mode = True

class StudentMedicalConditionAssociationBase(BaseModel):
    student_id: int
    medical_condition_id: int

class StudentMedicalConditionAssociationResponse(StudentMedicalConditionAssociationBase):
    pass

class StudentBase(BaseModel):
    name: str
    age: int
    # ... other student fields
    medical_conditions: List[MedicalConditionResponse] = []

class StudentResponse(StudentBase):
    id: int
    # ... other student fields
    medical_conditions: List[MedicalConditionResponse]

    class Config:
        orm_mode = True

class DailyActivityResponse(BaseModel):
    id: int
    date: datetime
    description: str
    notes: Optional[str]
    student_id: int


class DailyActivityRequest(BaseModel):
    date: Optional[datetime] = None
    description: str
    notes: Optional[str] = None
    student_id: int

class BillingBase(BaseModel):
    student_id: int
    amount: float
    due_date: datetime

class BillingCreate(BillingBase):
    pass

class BillingResponse(BillingBase):
    id: int
    status: str

class PaymentBase(BaseModel):
    bill_id: int
    amount_paid: float
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    payment_date: datetime

class ScheduleBase(BaseModel):
    staff_id: int
    day_of_week: str
    start_time: datetime
    end_time: datetime

class ScheduleResponse(ScheduleBase):
    id: int

class StaffRequest(BaseModel):
    name: str
    description: str
    age: int
    address: str
    gender_id: int
    class_id: int
    emergency_contact_id: int
    medical_condition_id: int
    is_disable: str
    image: str

class StaffResponse(BaseModel):
    id: int
    name: str
    description: str
    age: int
    address: str
    gender_id: int
    class_id: int
    emergency_contact_id: int
    medical_condition_id: int
    is_disable: str
    image: str
    schedule: List[ScheduleResponse] = []

class ScheduleCreate(ScheduleBase):
    pass

class ParentRegistration(BaseModel):
    name: str
    age: int
    email: str
    password: str

class ParentLogin(BaseModel):
    email: str
    password: str

class StaffCreate(BaseModel):
    name: str
    age: int
    gender_id: int
    address: str
    email: str
    phone: str
    password: str
    hashedpassword: str
    department_id: int
    role_id: int
    image: str

class StaffLogin(BaseModel):
    email: str
    password: str

class ParentCreate(BaseModel):
    name: str
    age: int
    gender_id: int
    address: str
    email: str
    phone: str
    password: str
    hashedpassword: str

class ParentLogin(BaseModel):
    email: str
    password: str