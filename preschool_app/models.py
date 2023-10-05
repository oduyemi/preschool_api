from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel


Base =  declarative_base()

class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Student(Base):
    __tablename__ = "student"
    age = Column(Integer, index=True)
    address = Column(Text, index=True)
    gender_id = Column(Integer, ForeignKey("gender_id"))
    class_id = Column(Integer, ForeignKey("class_id"))
    emergency_contact_id = Column(Integer, ForeignKey("emergency_id"))
    medical_condition_id = Column(Integer, ForeignKey("medical_id"))
    is_disable = Column(Boolean, default=False)
 
    classes = relationship("Class", secondary="class_student_association", back_populates="students")
    class_teacher_id = Column(Integer, ForeignKey("staff.id"))
    assistant_teacher_id = Column(Integer, ForeignKey("staff.id"))


class Parent(Base):
    __tablename__ = "parent"
    age = Column(Integer, index=True)
    gender_id = Column(Integer, ForeignKey("gender_id"))
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    password = Column(String, index=True)
    hashedpassword = Column(String)


class Emergency(Base):
    __tablename__ = "emergency" 
    phone = Column(String, index=True)


class Gender(Base):
    __tablename__ = "gender"
    __abstract__ = True
    

class MedicalCondition(Base):
    __tablename__ = "medical"
    __abstract__ = True


class Program(Base):
    __tablename__ = "program"
    description = Column(String, index=True)


class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    program_id = Column(Integer, ForeignKey("program_id"))

    students = relationship("Student", secondary="class_student_association", back_populates="classes")
    class_teacher = relationship("Staff", foreign_keys=[class_teacher_id], back_populates="classes_taught")
    assistant_teacher = relationship("Staff", foreign_keys=[assistant_teacher_id], back_populates="classes_assisted")
    program = relationship("Program", back_populates="classes")


class ClassStudentAssociation(Base):
    __tablename__ = "class_student_association"
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)



class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    gender_id = Column(Integer, ForeignKey("gender_id"))
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    password = Column(String, index=True)
    hashedpassword = Column(String)
    department = Column(Integer, ForeignKey("teacher_id"))
    role = Column(Integer, ForeignKey("teacher_id"))

    department = relationship("Department", foreign_keys=[department_id], back_populates="staff_members")
    staff_roles = relationship("Role", back_populates="staff_members")
    job_role = relationship("Role", foreign_keys=[role_id], back_populates="staff_roles")
    classes_taught = relationship("Class", foreign_keys=[Class.class_teacher_id], back_populates="class_teacher_staff")
    classes_assisted = relationship("Class", foreign_keys=[Class.assistant_teacher_id], back_populates="assistant_teacher_staff")


class Department(Base):
    __tablename__ = "department"  
    __abstract__ = True

    staff_roles = relationship("Staff", back_populates="job_role")


class Role(Base):
    __tablename__ = "role"
    __abstract__ = True

    staff_members = relationship("Staff", back_populates="department")
    
