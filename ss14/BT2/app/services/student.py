
from fastapi import HTTPException
from app.models.student import Student
def all(db): return db.query(Student).all()
def one(db,i):
 s=db.query(Student).filter(Student.id==i).first()
 if not s: raise HTTPException(404,"Student not found")
 return s
def create(db,d):
 s=Student(**d.model_dump());db.add(s);db.commit();db.refresh(s);return s
def update(db,i,d):
 s=one(db,i)
 for k,v in d.model_dump().items(): setattr(s,k,v)
 db.commit();db.refresh(s);return s
def delete(db,i):
 s=one(db,i);db.delete(s);db.commit();return {"message":"Deleted"}
