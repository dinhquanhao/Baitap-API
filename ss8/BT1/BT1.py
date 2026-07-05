from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Logistics API")

carriers=[
{"id":1,"code":"GHN","name":"Giao Hang Nhanh","max_weight_capacity":5000,"status":"ACTIVE"},
{"id":2,"code":"GHTK","name":"Giao Hang Tiet Kiem","max_weight_capacity":3000,"status":"ACTIVE"},
{"id":3,"code":"VTP","name":"Viettel Post","max_weight_capacity":10000,"status":"SUSPENDED"},
]
shipments=[{"id":1,"carrier_id":1,"order_reference":"ORD-2026-001","total_weight":4200,"dispatch_date":"2026-07-01","shift":"MORNING"}]
VALID_STATUS=["ACTIVE","INACTIVE","SUSPENDED"]
VALID_SHIFT=["MORNING","AFTERNOON","NIGHT"]
class Carrier(BaseModel):
    code:str
    name:str=Field(min_length=3)
    max_weight_capacity:int=Field(gt=0)
    status:str
class Shipment(BaseModel):
    carrier_id:int
    order_reference:str
    total_weight:int=Field(gt=0)
    dispatch_date:str
    shift:str

@app.post("/carriers")
def create_carrier(carrier:Carrier):
    if carrier.status not in VALID_STATUS: raise HTTPException(400,"Invalid status")
    if any(c["code"].lower()==carrier.code.lower() for c in carriers): raise HTTPException(400,"Carrier code already exists")
    d=carrier.dict(); d["id"]=len(carriers)+1; carriers.append(d); return d

@app.get("/carriers")
def get_carriers(keyword:Optional[str]=Query(None),status:Optional[str]=None,min_weight:Optional[int]=None):
    r=carriers
    if keyword:
        k=keyword.lower(); r=[c for c in r if k in c["code"].lower() or k in c["name"].lower()]
    if status: r=[c for c in r if c["status"]==status]
    if min_weight: r=[c for c in r if c["max_weight_capacity"]>=min_weight]
    return r

@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id:int):
    for c in carriers:
        if c["id"]==carrier_id: return c
    raise HTTPException(404,"Carrier not found")

@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id:int,carrier:Carrier):
    if carrier.status not in VALID_STATUS: raise HTTPException(400,"Invalid status")
    for i,c in enumerate(carriers):
        if c["id"]==carrier_id:
            if any(x["id"]!=carrier_id and x["code"].lower()==carrier.code.lower() for x in carriers): raise HTTPException(400,"Carrier code already exists")
            d=carrier.dict(); d["id"]=carrier_id; carriers[i]=d; return d
    raise HTTPException(404,"Carrier not found")

@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id:int):
    for i,c in enumerate(carriers):
        if c["id"]==carrier_id:
            del carriers[i]; return {"message":"Carrier deleted successfully"}
    raise HTTPException(404,"Carrier not found")

@app.post("/shipments")
def create_shipment(shipment:Shipment):
    if shipment.shift not in VALID_SHIFT: raise HTTPException(400,"Invalid shift")
    carrier=next((c for c in carriers if c["id"]==shipment.carrier_id),None)
    if not carrier: raise HTTPException(404,"Carrier not found")
    if carrier["status"]!="ACTIVE": raise HTTPException(400,"Carrier is not ACTIVE")
    if shipment.total_weight>carrier["max_weight_capacity"]: raise HTTPException(400,"Shipment weight exceeds carrier capacity")
    for s in shipments:
        if s["carrier_id"]==shipment.carrier_id and s["dispatch_date"]==shipment.dispatch_date and s["shift"]==shipment.shift:
            raise HTTPException(400,"Carrier already has a shipment in this shift")
    d=shipment.dict(); d["id"]=len(shipments)+1; shipments.append(d); return d

@app.get("/shipments")
def get_shipments():
    return shipments
