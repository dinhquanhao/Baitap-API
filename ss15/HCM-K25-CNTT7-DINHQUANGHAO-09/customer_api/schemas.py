
from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    customer_type: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
