from fastapi import FastAPI, HTTPException, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from .database import SessionLocal
from instance.config import SECRET_KEY, DATABASE_URI

starter = FastAPI(title="Storytime PreSchool", description="Providing childcare for children")


engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base: DeclarativeMeta = declarative_base()


from preschool_app import routes
starter.include_router(routes.preschool_router)
starter.include_router(routes.parent_router, prefix="/parent")
starter.include_router(routes.staff_router, prefix="/staff")

