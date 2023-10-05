from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from .database import SessionLocal
from instance.config import SECRET_KEY, DATABASE_URI

# from preschool_app import routes


starter = FastAPI()
router = APIRouter()

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base: DeclarativeMeta = declarative_base()

# starter.include_router(starter.router)