
from pydantic import BaseModel
class StudentCreate(BaseModel):
 full_name:str
 email:str
 major:str
 gpa:float
