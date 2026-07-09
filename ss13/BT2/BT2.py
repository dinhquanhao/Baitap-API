"""
BT2.py
API Hệ thống Đặt chỗ Dịch vụ Chăm sóc Thú cưng (Pet Boarding Slots)
5 API CRUD quản lý bảng boarding_slots (MySQL) qua SQLAlchemy + FastAPI.

Cách chạy:
    pip install fastapi uvicorn sqlalchemy pymysql pydantic
    uvicorn BT2:app --reload

Cấu hình kết nối MySQL: chỉnh biến DATABASE_URL bên dưới cho phù hợp với môi trường của bạn.
"""

from datetime import datetime, timezone
from typing import Optional, Literal, List, Any

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


# ==========================================================
# 1. CẤU HÌNH DATABASE (database.py được gộp vào đây cho gọn)
# ==========================================================
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/pet_boarding_db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# 2. MODEL (giữ nguyên cấu trúc đề bài cho sẵn)
# ==========================================================
class BoardingSlot(Base):
    __tablename__ = "boarding_slots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slot_number = Column(String(50), unique=True, nullable=False, index=True)
    room_size = Column(String(30), nullable=False)
    price_per_day = Column(Float, nullable=False)
    status = Column(String(30), default="VACANT", nullable=False)


Base.metadata.create_all(bind=engine)


# ==========================================================
# 3. PYDANTIC SCHEMAS
# ==========================================================
RoomSize = Literal["SMALL", "MEDIUM", "LARGE"]
SlotStatus = Literal["VACANT", "OCCUPIED"]


class BoardingSlotCreate(BaseModel):
    slot_number: str = Field(..., min_length=1, max_length=50)
    room_size: RoomSize
    price_per_day: float = Field(..., gt=0)
    status: SlotStatus = "VACANT"


class BoardingSlotUpdate(BaseModel):
    # Tất cả optional để phục vụ cập nhật từng phần (PATCH-style PUT)
    slot_number: Optional[str] = Field(default=None, min_length=1, max_length=50)
    room_size: Optional[RoomSize] = None
    price_per_day: Optional[float] = Field(default=None, gt=0)
    status: Optional[SlotStatus] = None


class BoardingSlotOut(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    class Config:
        from_attributes = True


# ==========================================================
# 4. CHUẨN HÓA RESPONSE (6 trường bắt buộc)
# ==========================================================
def build_response(
    status_code: int,
    message: str,
    error: Optional[str],
    data: Any,
    path: str,
) -> dict:
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


class AppException(Exception):
    """Exception nội bộ dùng để trả lỗi nghiệp vụ theo đúng format 6 trường."""

    def __init__(self, status_code: int, message: str, error: str):
        self.status_code = status_code
        self.message = message
        self.error = error


# ==========================================================
# 5. KHỞI TẠO APP + EXCEPTION HANDLERS
# ==========================================================
app = FastAPI(title="Pet Boarding Slots API")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=build_response(exc.status_code, exc.message, exc.error, None, str(request.url.path)),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=build_response(exc.status_code, str(exc.detail), "Error", None, str(request.url.path)),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Không để lỗi thô của MySQL/hệ thống lộ ra ngoài => trả message chung chung
    return JSONResponse(
        status_code=500,
        content=build_response(500, "Internal Server Error", "Internal Server Error", None, str(request.url.path)),
    )


# ==========================================================
# 6. HÀM TIỆN ÍCH
# ==========================================================
def get_slot_or_404(db: Session, slot_id: int) -> BoardingSlot:
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()
    if not slot:
        raise AppException(404, "Boarding slot not found", "Not Found")
    return slot


# ==========================================================
# 7. API CRUD
# ==========================================================

# ---- 7.1 POST /boarding-slots : Thêm khoang lưu trú mới ----
@app.post("/boarding-slots")
def create_boarding_slot(payload: BoardingSlotCreate, request: Request, db: Session = Depends(get_db)):
    existing = db.query(BoardingSlot).filter(BoardingSlot.slot_number == payload.slot_number).first()
    if existing:
        raise AppException(400, "Slot number already exists", "Bad Request")

    new_slot = BoardingSlot(**payload.model_dump())
    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
    except IntegrityError:
        db.rollback()
        raise AppException(400, "Slot number already exists", "Bad Request")
    except SQLAlchemyError:
        db.rollback()
        raise AppException(500, "Failed to create boarding slot", "Internal Server Error")

    data = BoardingSlotOut.model_validate(new_slot).model_dump()
    return build_response(201, "Tạo khoang lưu trú thành công", None, data, str(request.url.path))


# ---- 7.2 GET /boarding-slots : Lấy danh sách tất cả khoang lưu trú ----
@app.get("/boarding-slots")
def get_all_boarding_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(BoardingSlot).all()
    data: List[dict] = [BoardingSlotOut.model_validate(s).model_dump() for s in slots]
    return build_response(200, "Lấy danh sách thành công", None, data, str(request.url.path))


# ---- 7.3 GET /boarding-slots/{slot_id} : Lấy chi tiết một khoang lưu trú ----
@app.get("/boarding-slots/{slot_id}")
def get_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = get_slot_or_404(db, slot_id)
    data = BoardingSlotOut.model_validate(slot).model_dump()
    return build_response(200, "Lấy chi tiết thành công", None, data, str(request.url.path))


# ---- 7.4 PUT /boarding-slots/{slot_id} : Cập nhật thông tin khoang lưu trú ----
@app.put("/boarding-slots/{slot_id}")
def update_boarding_slot(
    slot_id: int, payload: BoardingSlotUpdate, request: Request, db: Session = Depends(get_db)
):
    slot = get_slot_or_404(db, slot_id)

    update_data = payload.model_dump(exclude_unset=True)

    # Nếu có đổi slot_number thì kiểm tra trùng với bản ghi khác
    if "slot_number" in update_data:
        duplicate = (
            db.query(BoardingSlot)
            .filter(BoardingSlot.slot_number == update_data["slot_number"], BoardingSlot.id != slot_id)
            .first()
        )
        if duplicate:
            raise AppException(400, "Slot number already exists", "Bad Request")

    for key, value in update_data.items():
        setattr(slot, key, value)

    try:
        db.commit()
        db.refresh(slot)
    except IntegrityError:
        db.rollback()
        raise AppException(400, "Slot number already exists", "Bad Request")
    except SQLAlchemyError:
        db.rollback()
        raise AppException(500, "Failed to update boarding slot", "Internal Server Error")

    data = BoardingSlotOut.model_validate(slot).model_dump()
    return build_response(200, "Cập nhật thành công", None, data, str(request.url.path))


# ---- 7.5 DELETE /boarding-slots/{slot_id} : Xóa khoang lưu trú ----
@app.delete("/boarding-slots/{slot_id}")
def delete_boarding_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = get_slot_or_404(db, slot_id)

    try:
        db.delete(slot)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise AppException(500, "Failed to delete boarding slot", "Internal Server Error")

    return build_response(200, "Xóa khoang lưu trú thành công", None, None, str(request.url.path))
