
from fastapi import HTTPException
from app.models.product import Product
def get_all(db): return db.query(Product).all()
def get_one(db,id):
 p=db.query(Product).filter(Product.id==id).first()
 if not p: raise HTTPException(404,"Product not found")
 return p
def create(db,data):
 p=Product(name=data.name,price=data.price);db.add(p);db.commit();db.refresh(p);return p
def update(db,id,data):
 p=get_one(db,id);p.name=data.name;p.price=data.price;db.commit();db.refresh(p);return p
def delete(db,id):
 p=get_one(db,id);db.delete(p);db.commit();return {"message":"Deleted"}
