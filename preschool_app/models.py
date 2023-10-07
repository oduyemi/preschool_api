from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, sessionmaker, registry
from sqlalchemy.ext.declarative import declarative_base
from preschool_app import Base, engine
from pydantic import BaseModel


Session = sessionmaker(bind=engine)
session = Session()

mapper_registry = registry()
mapper_registry.configure()

Base = declarative_base()



class Program(Base):
    __tablename__ = "program"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    description = Column(Text, index=True)

    classes = relationship("Class", back_populates="program")


class Emergency(Base):
    __tablename__ = "emergency" 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    phone = Column(String(length=80), index=True)


class Gender(Base):
    __tablename__ = "gender"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)


class MedicalCondition(Base):
    __tablename__ = "medical"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)


class Department(Base):
    __tablename__ = "department"  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)

    staff_members = relationship("Staff", back_populates="department")


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable = True) 



class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    age = Column(Integer, CheckConstraint("age >= 15"), index=True)
    gender_id = Column(Integer, ForeignKey("gender.id"))
    address = Column(Text, index=True)
    email = Column(String(length=120), unique=True, index=True)
    phone = Column(String(length=80), index=True)
    password = Column(String(length=100), index=True)
    hashedpassword = Column(String(length=100), index=True)
    department_id = Column(Integer, ForeignKey("department.id"))
    role_id = Column(Integer, ForeignKey("role.id"))
    image = Column(String(length=120), index=True)

    department = relationship("Department", back_populates="staff_members")
    teacher = relationship("Teacher", back_populates="staff")


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))

    staff = relationship("Staff", back_populates="teacher")
    class_taught = relationship("Class", secondary="teacher_class_association", back_populates="class_teacher")
    class_assisted = relationship("Class", secondary="teacher_class_association", back_populates="assistant_teacher")
    classes_taught = relationship("Class", secondary="teacher_class_association")


class TeacherClassAssociation(Base):
    __tablename__ = "teacher_class_association"
    teacher_id = Column(Integer, ForeignKey("teacher.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)


class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    program_id = Column(Integer, ForeignKey("program.id"))
    class_teacher_id = Column(Integer, ForeignKey("teacher.id"))
    assistant_teacher_id = Column(Integer, ForeignKey("teacher.id"))

    program = relationship("Program", back_populates="classes")
    class_student = relationship("Student", secondary="class_student_association", back_populates="student_class")
    students = relationship("Student", back_populates="class_deets")
    class_teacher = relationship("Teacher", secondary="teacher_class_association", back_populates="class_taught")
    assistant_teacher = relationship("Teacher", secondary="teacher_class_association", back_populates="class_assisted")


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    age = Column(Integer, CheckConstraint("age <= 10"), index=True)
    address = Column(Text, index=True)
    gender_id = Column(Integer, ForeignKey("gender.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    emergency_contact_id = Column(Integer, ForeignKey("emergency.id"))
    medical_condition_id = Column(Integer, ForeignKey("medical.id"))
    is_disable = Column(Boolean, default=False, index=True)
    image = Column(String(length=120), index=True)

    student_class = relationship("Class", secondary="class_student_association", back_populates="class_student")
    class_deets = relationship("Class", back_populates="students")


class ClassStudentAssociation(Base):
    __tablename__ = "class_student_association"
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)

Student.classes = relationship("Class", secondary="class_student_association", back_populates="students")
Class.students = relationship("Student", secondary="class_student_association", back_populates="classes")

class Admission(Base):
    __tablename__ = "admission"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    program_id = Column(Integer, ForeignKey("program.id"))
    student_number = Column(String(length=20), index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)

    def generate_student_number(self):
        year = str(datetime.utcnow().year)[-2:]
        program_identifiers = {1: "AA", 2: "BB", 3: "CC", 4: "DD", 5: "EE", 6: "FF"} 
        program_identifier = program_identifiers.get(str(self.program_id), "XX")
        student_id = str(self.student_id).zfill(3)

        self.student_number = f"{year}{program_identifier}/{student_id}"

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    age = Column(Integer, CheckConstraint("age >= 15"), index=True)
    gender_id = Column(Integer, ForeignKey("gender.id"))
    address = Column(Text)
    email = Column(String(length=120), unique=True, index=True)
    phone = Column(String(length=80), index=True)
    password = Column(String(length=100), index=True)
    hashedpassword = Column(String(length=100), index=True)



