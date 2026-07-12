
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate
from app.services import product as s
router=APIRouter(prefix="/products",tags=["Products"])
@router.get("")
def a(db:Session=Depends(get_db)): return s.get_all(db)
@router.get("/{product_id}")
def b(product_id:int,db:Session=Depends(get_db)): return s.get_one(db,product_id)
@router.post("")
def c(data:ProductCreate,db:Session=Depends(get_db)): return s.create(db,data)
@router.put("/{product_id}")
def d(product_id:int,data:ProductCreate,db:Session=Depends(get_db)): return s.update(db,product_id,data)
@router.delete("/{product_id}")
def e(product_id:int,db:Session=Depends(get_db)): return s.delete(db,product_id)
