from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, CheckConstraint, Float, func
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


class MedicalCategory(Base):
    __tablename__ = "medical_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)

    conditions = relationship("MedicalCondition", back_populates="medical_category")

class MedicalCondition(Base):
    __tablename__ = "medical"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    medical_category_id = Column(Integer, ForeignKey("medical_category.id"))

    medical_category = relationship("MedicalCategory", back_populates="conditions")




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
    medical_conditions = relationship("MedicalCondition", secondary="staff_medical_condition_association")
    schedule = relationship("Schedule", back_populates="staff")


class StaffMedicalConditionAssociation(Base):
    __tablename__ = "staff_medical_condition_association"
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    medical_condition_id = Column(Integer, ForeignKey("medical.id"), primary_key=True)


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))

    staff = relationship("Staff", back_populates="teacher")
    class_taught = relationship("Class", secondary="teacher_class_association", back_populates="class_teacher", overlaps='classes_taught')
    classes_taught = relationship("Class", secondary="teacher_class_association", overlaps='class_taught')
    class_assisted = relationship("Class", secondary="teacher_class_association", back_populates="assistant_teacher", overlaps='class_taught,classes_taught')



class TeacherClassAssociation(Base):
    __tablename__ = "teacher_class_association"
    teacher_id = Column(Integer, ForeignKey("teacher.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)


class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    program_id = Column(Integer, ForeignKey("program.id"))
    class_teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)
    assistant_teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)

    program = relationship("Program", back_populates="classes")
    students = relationship("Student", back_populates="class_deets")
    class_student = relationship("Student", secondary="class_student_association", back_populates="student_class", viewonly=True)
    class_teacher = relationship("Teacher", secondary="teacher_class_association", back_populates="class_taught", overlaps='assistant_teacher', viewonly=True)
    assistant_teacher = relationship("Teacher", secondary="teacher_class_association", back_populates="class_assisted", overlaps='class_teacher', viewonly=True)


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

    student_class = relationship("Class", secondary="class_student_association", back_populates="class_student", viewonly=True)
    class_deets = relationship("Class", back_populates="students")
    medical_conditions = relationship("MedicalCondition", secondary="student_medical_condition_association")
    bills = relationship("Billing", back_populates="student")
    payments = relationship("Payment", back_populates="student", foreign_keys="[Payment.student_id]")



Student.attendance = relationship("Attendance", back_populates="student")
Student.daily_activities = relationship("DailyActivity", back_populates="student", order_by="desc(DailyActivity.date)")



class ClassStudentAssociation(Base):
    __tablename__ = "class_student_association"
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)

Student.classes = relationship("Class", secondary="class_student_association", back_populates="students")
Class.students = relationship("Student", secondary="class_student_association", back_populates="classes")

class StudentMedicalConditionAssociation(Base):
    __tablename__ = "student_medical_condition_association"
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    medical_condition_id = Column(Integer, ForeignKey("medical.id"), primary_key=True)


class Admission(Base):
    __tablename__ = "admission"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    program_id = Column(Integer, ForeignKey("program.id"))
    student_number = Column(String(length=20), index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)

    def generate_student_number(self):
        year = str(datetime.utcnow().year)[-2:]
        program_identifiers = {1: "TL", 2: "SF", 3: "SM", 4: "DD", 5: "EE", 6: "FF"} 
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

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    status = Column(String(length=10), default="absent", index=True)  # "present" or "absent"

    student = relationship("Student", back_populates="attendance")


class DailyActivity(Base):
    __tablename__ = "daily_activity"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    description = Column(String(length=200), index=True)
    notes = Column(Text, nullable=True)
    student_id = Column(Integer, ForeignKey("student.id"))

    student = relationship("Student", back_populates="daily_activities")


class Billing(Base):
    __tablename__ = "billing"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    amount = Column(Float, index=True)
    due_date = Column(DateTime, index=True)
    status = Column(String(length=20), default="pending", index=True)  # "paid", "pending", "overdue"

    student = relationship("Student", back_populates="bills")
    payments = relationship("Payment", back_populates="bill")  

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("billing.id"))
    payment_date = Column(DateTime, default=func.now(), index=True)
    amount_paid = Column(Float, index=True)
    payment_method = Column(String(length=20), index=True)  # "credit_card", "bank_transfer", etc.

    student_id = Column(Integer, ForeignKey("student.id"))
    student = relationship("Student", back_populates="payments", primaryjoin="Payment.student_id == Student.id")

    bill = relationship("Billing", back_populates="payments")



class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    day_of_week = Column(String(length=20), index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    staff = relationship("Staff", back_populates="schedule")