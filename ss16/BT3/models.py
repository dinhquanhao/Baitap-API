from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
class Enrollment(Base):
 __tablename__="enrollments"
 id=Column(Integer,primary_key=True)
 student_id=Column(Integer,ForeignKey("students.id"))
 course_id=Column(Integer,ForeignKey("courses.id"))
 enrolled_at=Column(DateTime,default=datetime.utcnow)
 student=relationship("Student",back_populates="enrollments")
 course=relationship("Course",back_populates="enrollments")
class Student(Base):
 __tablename__="students"
 id=Column(Integer,primary_key=True)
 full_name=Column(String(100),nullable=False)
 status=Column(String(20),default="ACTIVE")
 enrollments=relationship("Enrollment",back_populates="student")
 courses=relationship("Course",secondary="enrollments",viewonly=True,back_populates="students")
class Course(Base):
 __tablename__="courses"
 id=Column(Integer,primary_key=True)
 name=Column(String(100),unique=True,nullable=False)
 max_students=Column(Integer,nullable=False)
 enrollments=relationship("Enrollment",back_populates="course")
 students=relationship("Student",secondary="enrollments",viewonly=True,back_populates="courses")
