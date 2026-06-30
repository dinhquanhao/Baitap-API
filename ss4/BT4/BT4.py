from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Student Registration API")

students = [{
    "full_name":"Existing User",
    "email":"existing@gmail.com",
    "age":22,
    "course":"python",
    "phone":"0912345678"
}]

class Student(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=1)
    course: str
    phone: str

@app.post("/students")
def create_student(student: Student):
    for s in students:
        if s["email"].lower() == student.email.lower():
            raise HTTPException(status_code=400, detail="Email đã tồn tại trong hệ thống")
    students.append(student.model_dump())
    return {"message":"Thêm học viên thành công","student":student}
