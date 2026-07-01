
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Laptop Dell",
        "price": 15000000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse Logitech",
        "price": 350000,
        "stock": 50
    }
]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: float
    stock: int

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    for p in products:
        if p["code"] == product.code:
            raise HTTPException(
                status_code=400,
                detail="Product code already exists"
            )

    new_product = {
        "id": len(products) + 1,
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }

"""
Phần 1 - Test case

| STT | Dữ liệu gửi lên | Kết quả hiện tại | Kết quả đúng mong muốn | Lỗi phát hiện |
|-----|------------------|------------------|-------------------------|---------------|
| 1 | code="SP001" | Vẫn tạo được sản phẩm mới | Báo lỗi 400 - Product code already exists | Không kiểm tra trùng mã |
| 2 | code="SP002" | Vẫn tạo được sản phẩm mới | Báo lỗi 400 - Product code already exists | Không kiểm tra trùng mã |

Khi gửi code mới:
- Code trùng -> HTTP 400
- Code mới -> Tạo thành công, HTTP 201 Created
"""
