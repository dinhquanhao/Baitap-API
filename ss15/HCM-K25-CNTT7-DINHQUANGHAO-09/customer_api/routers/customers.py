"""Các endpoint API liên quan tới khách hàng (/customers)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db
from response import api_response

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("")
def read_customers(db: Session = Depends(get_db)):
    """API 2: Lấy toàn bộ danh sách khách hàng."""
    customers = crud.get_customers(db)
    data = [schemas.CustomerOut.model_validate(c).model_dump() for c in customers]
    return api_response(200, "Lấy danh sách khách hàng thành công", data)


# Lưu ý: route /search phải khai báo TRƯỚC route /{customer_id}
# để tránh bị FastAPI hiểu nhầm "search" là một customer_id.
@router.get("/search")
def search_customers(customer_type: str, db: Session = Depends(get_db)):
    """API 3: Tìm kiếm gần đúng khách hàng theo nhóm (customer_type)."""
    customers = crud.search_customers_by_type(db, customer_type)
    data = [schemas.CustomerOut.model_validate(c).model_dump() for c in customers]
    return api_response(200, "Tìm kiếm khách hàng thành công", data)


@router.get("/{customer_id}")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """API 4: Lấy chi tiết khách hàng theo id."""
    customer = crud.get_customer(db, customer_id)
    if not customer:
        return api_response(404, "Không tìm thấy khách hàng", None, error="Not Found")
    data = schemas.CustomerOut.model_validate(customer).model_dump()
    return api_response(200, "Lấy chi tiết khách hàng thành công", data)


@router.post("")
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """API 5: Thêm mới một khách hàng."""
    new_customer = crud.create_customer(db, customer)
    data = schemas.CustomerOut.model_validate(new_customer).model_dump()
    return api_response(201, "Thêm khách hàng thành công", data)


@router.put("/{customer_id}")
def update_customer(
    customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    """API 6: Cập nhật toàn bộ thông tin khách hàng theo id."""
    updated = crud.update_customer(db, customer_id, customer)
    if not updated:
        return api_response(404, "Không tìm thấy khách hàng", None, error="Not Found")
    data = schemas.CustomerOut.model_validate(updated).model_dump()
    return api_response(200, "Cập nhật khách hàng thành công", data)


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """API 7: Xóa khách hàng theo id."""
    deleted = crud.delete_customer(db, customer_id)
    if not deleted:
        return api_response(404, "Không tìm thấy khách hàng", None, error="Not Found")
    return api_response(200, "Xóa khách hàng thành công", None)
