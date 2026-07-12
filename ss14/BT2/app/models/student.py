
from sqlalchemy import Column,Integer,String,Float
from app.database import Base
class Student(Base):
 __tablename__="students"
 id=Column(Integer,primary_key=True,index=True)
 full_name=Column(String(255))
 email=Column(String(255))
 major=Column(String(255))
 gpa=Column(Float)
