from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
engine=create_engine("mysql+pymysql://user:pass@localhost/db")
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()