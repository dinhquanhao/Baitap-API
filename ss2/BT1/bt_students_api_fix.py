from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

# Endpoint RESTful trả về danh sách sinh viên dưới dạng JSON array
@app.get("/students")
def get_students():
    return students


"""
PHÂN TÍCH LỖI LEGACY CODE

Ví dụ code cũ:
@app.get("/getStudents")
def get_students():
    return "Nguyen Van A, Tran Thi B, Le Van C"

Lỗi:
1. Endpoint /getStudents không theo chuẩn RESTful.
   Nên dùng danh từ số nhiều: /students

2. API trả về string thay vì JSON array.
   Frontend mong đợi:
   [
       {"id":1,"name":"Nguyen Van A"},
       ...
   ]

3. Không nên dùng string concat để trả dữ liệu vì frontend
   không thể duyệt dữ liệu bằng map(), forEach()...
"""
