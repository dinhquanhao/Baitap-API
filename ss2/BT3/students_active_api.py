from fastapi import FastAPI

app = FastAPI()

# Danh sách sinh viên
students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

"""
PHẦN 1: BÁO CÁO PHÂN TÍCH

1. Input:
- Danh sách students chứa thông tin id, name và status.

2. Output:
- API trả về message và data chứa danh sách sinh viên đang học.

3. Điều kiện xác định sinh viên đang học:
- status == "active"

4. Các bước xử lý:
- Nhận request GET /students/active
- Duyệt danh sách students
- Lọc các sinh viên có status = "active"
- Nếu có dữ liệu thì trả về danh sách sinh viên đang học
- Nếu không có dữ liệu thì trả về message và danh sách rỗng
"""

# API lấy danh sách sinh viên đang học
@app.get("/students/active")
def get_active_students():
    active_students = [
        student for student in students
        if student["status"] == "active"
    ]

    if not active_students:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }
