from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base
employee_project=Table("employee_project",Base.metadata,
Column("employee_id",Integer,ForeignKey("employees.id"),primary_key=True),
Column("project_id",Integer,ForeignKey("projects.id"),primary_key=True))
class Department(Base):
 __tablename__="departments"
 id=Column(Integer,primary_key=True,index=True)
 name=Column(String(100),nullable=False)
 employees=relationship("Employee",back_populates="department")
class Employee(Base):
 __tablename__="employees"
 id=Column(Integer,primary_key=True,index=True)
 name=Column(String(100),nullable=False)
 department_id=Column(Integer,ForeignKey("departments.id"))
 department=relationship("Department",back_populates="employees")
 device=relationship("Device",back_populates="employee",uselist=False)
 projects=relationship("Project",secondary=employee_project,back_populates="employees")
class Device(Base):
 __tablename__="devices"
 id=Column(Integer,primary_key=True,index=True)
 serial_number=Column(String(50),unique=True,nullable=False)
 employee_id=Column(Integer,ForeignKey("employees.id"),unique=True)
 employee=relationship("Employee",back_populates="device")
class Project(Base):
 __tablename__="projects"
 id=Column(Integer,primary_key=True,index=True)
 title=Column(String(100),nullable=False)
 employees=relationship("Employee",secondary=employee_project,back_populates="projects")
