from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Double
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

DATABASE_URL = "mysql+pymysql://root:123456@localhost/smart_home_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class SmartHomePlan(Base):
    __tablename__ = "smart_home_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_code = Column(String(50), unique=True, nullable=False)
    plan_name = Column(String(255), nullable=False)
    device_quantity = Column(Integer, nullable=False)
    price = Column(Double, nullable=False)


Base.metadata.create_all(bind=engine)


class SmartHomePlanCreate(BaseModel):
    plan_code: str = Field(..., min_length=1)
    plan_name: str = Field(..., min_length=1)
    device_quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


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


@app.post("/smart-home-plans", status_code=201)
def create_plan(plan: SmartHomePlanCreate, request: Request, db: Session = Depends(get_db)):
    new_plan = SmartHomePlan(
        plan_code=plan.plan_code,
        plan_name=plan.plan_name,
        device_quantity=plan.device_quantity,
        price=plan.price
    )

    try:
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        return response(
            201,
            "Thêm gói thiết bị thành công",
            None,
            {
                "id": new_plan.id,
                "plan_code": new_plan.plan_code,
                "plan_name": new_plan.plan_name,
                "device_quantity": new_plan.device_quantity,
                "price": new_plan.price
            },
            request.url.path
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Plan code already exists")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/smart-home-plans")
def get_all_plans(request: Request, db: Session = Depends(get_db)):
    plans = db.query(SmartHomePlan).all()

    data = []

    for plan in plans:
        data.append({
            "id": plan.id,
            "plan_code": plan.plan_code,
            "plan_name": plan.plan_name,
            "device_quantity": plan.device_quantity,
            "price": plan.price
        })

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        data,
        request.url.path
    )


@app.get("/smart-home-plans/{plan_id}")
def get_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    plan = db.query(SmartHomePlan).filter(SmartHomePlan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return response(
        200,
        "Lấy chi tiết thành công",
        None,
        {
            "id": plan.id,
            "plan_code": plan.plan_code,
            "plan_name": plan.plan_name,
            "device_quantity": plan.device_quantity,
            "price": plan.price
        },
        request.url.path
    )