from pydantic import BaseModel
from datetime import datetime
class EnrollmentCreate(BaseModel): student_id:int; course_id:int
class EnrollmentResponse(EnrollmentCreate):
 id:int; enrolled_at:datetime
 class Config: from_attributes=True
class CourseOut(BaseModel):
 id:int; name:str
 class Config: from_attributes=True
class StudentCourses(BaseModel):
 student_id:int; full_name:str; courses:list[CourseOut]
 class Config: from_attributes=True
