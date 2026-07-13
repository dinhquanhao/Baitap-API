
from fastapi import FastAPI

from database import Base, engine
from routers import customers
from response import api_response

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Management API",
    description="API quản lý thông tin khách hàng (họ tên, email, sđt, nhóm khách hàng).",
    version="1.0.0",
)

app.include_router(customers.router)


@app.get("/")
def root():
    return api_response(200, "API đang chạy", None)
