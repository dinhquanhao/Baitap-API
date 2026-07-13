# Customer Management API

API quản lý thông tin khách hàng, xây dựng bằng **FastAPI** + **MySQL** (SQLAlchemy).

## Cấu trúc thư mục

```
customer_api/
├── main.py             # Điểm khởi chạy app, gồm API kiểm tra server
├── database.py          # Kết nối MySQL, khởi tạo session
├── models.py             # SQLAlchemy model (bảng customers)
├── schemas.py            # Pydantic schema validate request/response
├── crud.py                # Hàm thao tác CRUD với database
├── response.py            # Hàm tạo response JSON theo chuẩn chung
├── routers/
│   ├── __init__.py
│   └── customers.py       # Toàn bộ endpoint /customers
├── requirements.txt
└── .env.example
```

## 1. Cài đặt

```bash
pip install -r requirements.txt
```

## 2. Chuẩn bị database

Tạo database MySQL trước khi chạy app (bảng `customers` sẽ tự được tạo khi app khởi động):

```sql
CREATE DATABASE customer_db;
```

## 3. Cấu hình kết nối

Copy `.env.example` thành `.env` (hoặc set biến môi trường trực tiếp) và điền thông tin MySQL của bạn:

```
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=customer_db
```

> Nếu không set biến môi trường, app sẽ mặc định dùng `root` / không mật khẩu / `localhost:3306` / `customer_db`.

## 4. Chạy chương trình

```bash
uvicorn main:app --reload
```

## 5. Test API

Mở Swagger UI tại: http://127.0.0.1:8000/docs

## Danh sách API

| STT | Chức năng | Method | Endpoint |
|---|---|---|---|
| 1 | Kiểm tra server | GET | `/` |
| 2 | Lấy danh sách khách hàng | GET | `/customers` |
| 3 | Tìm kiếm khách hàng theo nhóm | GET | `/customers/search?customer_type=...` |
| 4 | Lấy chi tiết khách hàng | GET | `/customers/{customer_id}` |
| 5 | Thêm khách hàng | POST | `/customers` |
| 6 | Cập nhật khách hàng | PUT | `/customers/{customer_id}` |
| 7 | Xóa khách hàng | DELETE | `/customers/{customer_id}` |

Tất cả API trả về JSON theo cấu trúc chuẩn:

```json
{
  "statusCode": 200,
  "error": null,
  "message": "...",
  "data": null
}
```
