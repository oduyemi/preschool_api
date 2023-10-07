from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from preschool_app import Base, engine

Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

# class BaseMixin:
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(length=200), index=True)

class Program(Base):
    __tablename__ = "program"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    description = Column(Text, index=True)

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

    staff_members = relationship("Staff", back_populates="role")

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))

    staff = relationship("Staff", back_populates="teacher")
    classes_taught = relationship("Class", secondary="teacher_class_association", back_populates="teachers")
    classes_assisted = relationship(
        "Class",
        secondary="teacher_class_association",
        primaryjoin="and_(Teacher.id == TeacherClassAssociation.teacher_id, Teacher.staff_id == TeacherClassAssociation.assistant_teacher_id)",
        secondaryjoin="Class.id == TeacherClassAssociation.class_id",
        back_populates="assistant_teachers"
    )


class TeacherClassAssociation(Base):
    __tablename__ = "teacher_class_association"
    teacher_id = Column(Integer, ForeignKey("teacher.id"), primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"), primary_key=True)
    assistant_teacher_id = Column(Integer, ForeignKey("staff.id"))



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
    role = relationship("Role", back_populates="staff_members")

    students_taught = relationship("Student", foreign_keys="Student.class_teacher_id", back_populates="class_teacher")
    students_assisted = relationship("Student", foreign_keys="Student.assistant_teacher_id", back_populates="assistant_teacher")
    teacher = relationship("Teacher", back_populates="staff")



class Class(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    description = Column(Text, index=True)
    program_id = Column(Integer, ForeignKey("program.id"))
    class_teacher_id = Column(Integer, ForeignKey("staff.id"))
    assistant_teacher_id = Column(Integer, ForeignKey("staff.id"))

    teachers = relationship("Teacher", secondary="teacher_class_association", back_populates="classes_taught")
    assistant_teachers = relationship("Teacher", secondary="teacher_class_association", back_populates="classes_assisted")
    class_teacher = relationship("Staff", foreign_keys=[class_teacher_id], back_populates="classes_taught")
    assistant_teacher = relationship("Staff", foreign_keys=[assistant_teacher_id], back_populates="classes_assisted")
    program = relationship("Program", back_populates="classes")

Class.students = relationship("Student", secondary="class_student_association", back_populates="classes")


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

    classes_taught = relationship("Class", secondary="class_student_association", back_populates="students")
    class_teacher_id = Column(Integer, ForeignKey("staff.id"))
    assistant_teacher_id = Column(Integer, ForeignKey("staff.id"))

    class_teacher = relationship("Staff", foreign_keys=[class_teacher_id], back_populates="students_taught")
    assistant_teacher = relationship("Staff", foreign_keys=[assistant_teacher_id], back_populates="students_assisted")


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


new_admission = Admission()
new_admission.generate_student_number()
session.add(new_admission)
session.commit()

class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), index=True)
    age = Column(Integer, CheckConstraint("age >= 15"), index=True)
    gender_id = Column(Integer, ForeignKey("gender_id"))
    address = Column(Text)
    email = Column(String(length=120), unique=True, index=True)
    phone = Column(String(length=80), index=True)
    password = Column(String(length=100), index=True)
    hashedpassword = Column(String(length=100), index=True)



