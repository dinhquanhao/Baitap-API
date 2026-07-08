from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:123456@localhost/medical_devices_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class MedicalDevice(Base):
    __tablename__ = "medical_devices"

    id = Column(Integer, primary_key=True, index=True)
    device_code = Column(String(50), unique=True, nullable=False)
    device_name = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    status = Column(Enum("ACTIVE", "INACTIVE"), default="ACTIVE", nullable=False)


Base.metadata.create_all(bind=engine)


class MedicalDeviceCreate(BaseModel):
    device_code: str = Field(..., min_length=1)
    device_name: str = Field(..., min_length=3)
    department: str = Field(..., min_length=1)
    status: Literal["ACTIVE", "INACTIVE"] = "ACTIVE"


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/devices", status_code=201)
def create_device(device: MedicalDeviceCreate, request: Request, db: Session = Depends(get_db)):
    new_device = MedicalDevice(
        device_code=device.device_code,
        device_name=device.device_name,
        department=device.department,
        status=device.status
    )

    try:
        db.add(new_device)
        db.commit()
        db.refresh(new_device)

        return response(
            201,
            "Thêm thiết bị y tế thành công",
            None,
            {
                "id": new_device.id,
                "device_code": new_device.device_code,
                "device_name": new_device.device_name,
                "department": new_device.department,
                "status": new_device.status
            },
            request.url.path
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Device code already exists")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/devices")
def get_all_devices(request: Request, db: Session = Depends(get_db)):
    devices = db.query(MedicalDevice).all()

    data = []

    for device in devices:
        data.append({
            "id": device.id,
            "device_code": device.device_code,
            "device_name": device.device_name,
            "department": device.department,
            "status": device.status
        })

    return response(
        200,
        "Lấy danh sách thiết bị y tế thành công",
        None,
        data,
        request.url.path
    )


@app.get("/devices/{device_id}")
def get_device(device_id: int, request: Request, db: Session = Depends(get_db)):
    device = db.query(MedicalDevice).filter(MedicalDevice.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return response(
        200,
        "Lấy chi tiết thiết bị y tế thành công",
        None,
        {
            "id": device.id,
            "device_code": device.device_code,
            "device_name": device.device_name,
            "department": device.department,
            "status": device.status
        },
        request.url.path
    )