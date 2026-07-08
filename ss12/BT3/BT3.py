from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/shipping_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True)
    tracking_code = Column(String(50), unique=True, nullable=False)
    receiver_name = Column(String(100), nullable=False)
    delivery_address = Column(String(255), nullable=False)


class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def update_shipment_service(
    db: Session,
    shipment_id: int,
    shipment_update: ShipmentUpdate
):
    shipment = db.query(ShipmentModel).filter(
        ShipmentModel.id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    shipment.receiver_name = shipment_update.receiver_name
    shipment.delivery_address = shipment_update.delivery_address

    db.commit()
    db.refresh(shipment)

    return shipment


app = FastAPI()


@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    db: Session = Depends(get_db)
):
    shipment = update_shipment_service(
        db,
        shipment_id,
        shipment_update
    )

    return {
        "message": "Shipment updated successfully",
        "data": {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "receiver_name": shipment.receiver_name,
            "delivery_address": shipment.delivery_address
        }
    }