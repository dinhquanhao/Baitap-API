# BT2.py

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


# ==========================
# GET: Danh sách học viên
# Có hỗ trợ tìm kiếm và lọc
# ==========================
@app.get("/students")
def get_students(
    keyword: str = None,
    min_age: int = None,
    max_age: int = None
):
    result = students

    if keyword:
        result = [
            student for student in result
            if keyword.lower() in student["name"].lower()
            or keyword.lower() in student["code"].lower()
            or keyword.lower() in student["email"].lower()
        ]

    if min_age is not None:
        result = [
            student for student in result
            if student["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            student for student in result
            if student["age"] <= max_age
        ]

    return result


# ==========================
# GET: Chi tiết học viên
# ==========================
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    return {"message": "Không tìm thấy học viên"}


# ==========================
# POST: Thêm học viên
# ==========================
@app.post("/students")
def create_student(student: dict):
    students.append(student)
    return {
        "message": "Thêm học viên thành công",
        "data": student
    }


# ==========================
# PUT: Cập nhật học viên
# ==========================
@app.put("/students/{student_id}")
def update_student(student_id: int, new_student: dict):
    for i in range(len(students)):
        if students[i]["id"] == student_id:
            students[i] = new_student
            return {
                "message": "Cập nhật thành công",
                "data": new_student
            }

    return {"message": "Không tìm thấy học viên"}


# ==========================
# DELETE: Xóa học viên
# ==========================
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i in range(len(students)):
        if students[i]["id"] == student_id:
            deleted_student = students.pop(i)
            return {
                "message": "Xóa thành công",
                "data": deleted_student
            }

    return {"message": "Không tìm thấy học viên"}