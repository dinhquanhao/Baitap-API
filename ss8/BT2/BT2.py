from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel,Field
from typing import Optional
import re
app=FastAPI(title="IT Asset Management")
assets=[
{"id":1,"serial_number":"SN-MAC-01","model":"MacBook Pro M3","stock_available":5,"status":"READY"},
{"id":2,"serial_number":"SN-DELL-02","model":"Dell UltraSharp 27","stock_available":10,"status":"READY"},
{"id":3,"serial_number":"SN-THINK-03","model":"ThinkPad X1 Carbon","stock_available":0,"status":"REPAIRING"}]
allocations=[{"id":1,"asset_id":1,"employee_email":"dev.nguyen@company.com","allocated_quantity":1,"start_date":"2026-07-01","duration_months":12}]
VALID=["READY","ALLOCATED","REPAIRING","SCRAPPED"]
EMAIL=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
class Asset(BaseModel):
    serial_number:str
    model:str=Field(min_length=2,max_length=255)
    stock_available:int=Field(ge=0)
    status:str
class Allocation(BaseModel):
    asset_id:int
    employee_email:str
    allocated_quantity:int=Field(gt=0)
    start_date:str
    duration_months:int
@app.post("/assets")
def create(a:Asset):
    if a.status not in VALID: raise HTTPException(400,"Invalid status")
    if any(x["serial_number"].lower()==a.serial_number.lower() for x in assets): raise HTTPException(400,"Serial already exists")
    d=a.dict(); d["id"]=len(assets)+1; assets.append(d); return d
@app.get("/assets")
def get(keyword:Optional[str]=None,status:Optional[str]=None,min_stock:Optional[int]=None):
    r=assets
    if keyword:
        k=keyword.lower(); r=[x for x in r if k in x["serial_number"].lower() or k in x["model"].lower()]
    if status: r=[x for x in r if x["status"]==status]
    if min_stock is not None: r=[x for x in r if x["stock_available"]>=min_stock]
    return r
@app.get("/assets/{asset_id}")
def one(asset_id:int):
    for a in assets:
        if a["id"]==asset_id:return a
    raise HTTPException(404,"Asset not found")
@app.put("/assets/{asset_id}")
def update(asset_id:int,a:Asset):
    if a.status not in VALID: raise HTTPException(400,"Invalid status")
    for i,x in enumerate(assets):
        if x["id"]==asset_id:
            if any(y["id"]!=asset_id and y["serial_number"].lower()==a.serial_number.lower() for y in assets): raise HTTPException(400,"Serial already exists")
            d=a.dict(); d["id"]=asset_id; assets[i]=d; return d
    raise HTTPException(404,"Asset not found")
@app.delete("/assets/{asset_id}")
def delete(asset_id:int):
    for i,x in enumerate(assets):
        if x["id"]==asset_id:
            del assets[i]; return {"message":"Asset deleted successfully"}
    raise HTTPException(404,"Asset not found")
@app.post("/allocations")
def alloc(al:Allocation):
    asset=next((x for x in assets if x["id"]==al.asset_id),None)
    if not asset: raise HTTPException(404,"Asset not found")
    if asset["status"]!="READY": raise HTTPException(400,"Asset is not READY")
    if al.allocated_quantity>asset["stock_available"]: raise HTTPException(400,"Not enough stock")
    if not re.match(EMAIL,al.employee_email): raise HTTPException(400,"Invalid email")
    if not 1<=al.duration_months<=12: raise HTTPException(400,"Duration must be from 1 to 12 months")
    asset["stock_available"]-=al.allocated_quantity
    d=al.dict(); d["id"]=len(allocations)+1; allocations.append(d); return d
@app.get("/allocations")
def get_allocations():
    return allocations
