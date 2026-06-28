from fastapi import FastAPI

app = FastAPI()

# Danh sách sinh viên
students = [
    {"id": 1, "name": "Nguyen Van A", "class": "CNTT1"},
    {"id": 2, "name": "Tran Thi B", "class": "CNTT1"},
    {"id": 3, "name": "Le Van C", "class": "CNTT2"}
]

# Endpoint chuẩn RESTful sử dụng GET để lấy dữ liệu
@app.get("/students")
def get_students():
    return students


"""
PHÂN TÍCH LỖI LEGACY CODE

Ví dụ mã cũ:

@app.get("/getStudents")
def get_students():
    return "Nguyen Van A, Tran Thi B, Le Van C"

1. Trace luồng xử lý:
- Frontend gọi GET /getStudents
- FastAPI thực thi hàm get_students()
- Hàm trả về kiểu string
- Frontend nhận được chuỗi thay vì JSON array
- Frontend không thể duyệt dữ liệu để hiển thị danh sách

2. Vì sao không nên trả về string:
- API thường trao đổi dữ liệu bằng JSON
- Frontend mong đợi một list để sử dụng map() hoặc vòng lặp
- String khó mở rộng khi cần thêm id, lớp hoặc thông tin khác

3. Lỗi REST endpoint:
- Sai: /getStudents
- Đúng: /students

RESTful API sử dụng danh từ đại diện cho tài nguyên thay vì động từ.
"""
