"""Pydantic schema dùng cho validate dữ liệu request/response."""
from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    customer_type: str


class CustomerCreate(CustomerBase):
    """Dữ liệu nhận vào khi tạo khách hàng mới (không kèm id)."""
    pass


class CustomerUpdate(CustomerBase):
    """Dữ liệu nhận vào khi cập nhật khách hàng."""
    pass


class CustomerOut(CustomerBase):
    """Dữ liệu trả về cho client, có kèm id."""
    id: int

    model_config = ConfigDict(from_attributes=True)
