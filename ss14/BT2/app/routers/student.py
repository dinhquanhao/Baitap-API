
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student import StudentCreate
from app.services import student as sv
router=APIRouter(prefix="/students",tags=["Students"])
@router.get("")
def a(db:Session=Depends(get_db)): return sv.all(db)
@router.get("/{student_id}")
def b(student_id:int,db:Session=Depends(get_db)): return sv.one(db,student_id)
@router.post("")
def c(data:StudentCreate,db:Session=Depends(get_db)): return sv.create(db,data)
@router.put("/{student_id}")
def d(student_id:int,data:StudentCreate,db:Session=Depends(get_db)): return sv.update(db,student_id,data)
@router.delete("/{student_id}")
def e(student_id:int,db:Session=Depends(get_db)): return sv.delete(db,student_id)
