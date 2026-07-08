from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:123456@localhost/parking_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


class ParkingSlotCreate(BaseModel):
    slot_code: str = Field(..., min_length=1)
    zone_name: str = Field(..., min_length=3)
    max_weight: int = Field(..., gt=0)
    is_available: bool = True


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


@app.post("/parking-slots", status_code=201)
def create_slot(slot: ParkingSlotCreate, request: Request, db: Session = Depends(get_db)):
    parking_slot = ParkingSlot(
        slot_code=slot.slot_code,
        zone_name=slot.zone_name,
        max_weight=slot.max_weight,
        is_available=slot.is_available
    )

    try:
        db.add(parking_slot)
        db.commit()
        db.refresh(parking_slot)

        return response(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            {
                "id": parking_slot.id,
                "slot_code": parking_slot.slot_code,
                "zone_name": parking_slot.zone_name,
                "max_weight": parking_slot.max_weight,
                "is_available": parking_slot.is_available
            },
            request.url.path
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="slot_code already exists")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/parking-slots")
def get_all_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(ParkingSlot).all()

    data = []

    for slot in slots:
        data.append({
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        })

    return response(
        200,
        "Lấy danh sách vị trí đỗ xe thành công",
        None,
        data,
        request.url.path
    )


@app.get("/parking-slots/{slot_id}")
def get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")

    return response(
        200,
        "Lấy chi tiết vị trí đỗ xe thành công",
        None,
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        },
        request.url.path
    )