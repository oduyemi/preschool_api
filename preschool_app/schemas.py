from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Union

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
    staff_id: Optional[int]

class GenderRequest(BaseModel):
    name: str

class GenderResponse(BaseModel):
    id: int
    name: str

