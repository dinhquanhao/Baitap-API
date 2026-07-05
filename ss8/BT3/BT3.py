from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

app = FastAPI(title="IT Asset Management API")

# ==========================
# Dữ liệu mẫu
# ==========================

assets = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": "READY"
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": "READY"
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": "REPAIRING"
    }
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

STATUS = ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]


# ==========================
# Model
# ==========================

class Asset(BaseModel):
    serial_number: str
    model: str = Field(..., min_length=2, max_length=255)
    stock_available: int = Field(..., ge=0)
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value not in STATUS:
            raise ValueError(
                "Status must be READY, ALLOCATED, REPAIRING or SCRAPPED"
            )
        return value


class Allocation(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(..., gt=0)
    start_date: str
    duration_months: int = Field(..., ge=1, le=12)

    @field_validator("employee_email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value


# ==========================
# API Assets
# ==========================

@app.post("/assets")
def create_asset(asset: Asset):

    for item in assets:
        if item["serial_number"] == asset.serial_number:
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_asset = asset.model_dump()
    new_asset["id"] = len(assets) + 1

    assets.append(new_asset)
    return new_asset


@app.get("/assets")
def get_assets(
    keyword: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_stock: Optional[int] = Query(None)
):

    result = assets

    if keyword:
        keyword = keyword.lower()
        result = [
            item for item in result
            if keyword in item["serial_number"].lower()
            or keyword in item["model"].lower()
        ]

    if status:
        result = [
            item for item in result
            if item["status"] == status
        ]

    if min_stock is not None:
        result = [
            item for item in result
            if item["stock_available"] >= min_stock
        ]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):

    for item in assets:
        if item["id"] == asset_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset: Asset):

    for item in assets:

        if item["id"] != asset_id and item["serial_number"] == asset.serial_number:
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    for index, item in enumerate(assets):
        if item["id"] == asset_id:
            update_data = asset.model_dump()
            update_data["id"] = asset_id
            assets[index] = update_data
            return update_data

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):

    for index, item in enumerate(assets):
        if item["id"] == asset_id:
            del assets[index]
            return {"message": "Asset deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


# ==========================
# API Allocations
# ==========================

@app.post("/allocations")
def create_allocation(allocation: Allocation):

    asset = None

    for item in assets:
        if item["id"] == allocation.asset_id:
            asset = item
            break

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Asset is not ready for allocation"
        )

    if allocation.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    asset["stock_available"] -= allocation.allocated_quantity

    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    new_allocation = allocation.model_dump()
    new_allocation["id"] = len(allocations) + 1

    allocations.append(new_allocation)

    return new_allocation


@app.get("/allocations")
def get_allocations():
    return allocations