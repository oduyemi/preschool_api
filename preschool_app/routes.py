from fastapi import APIRouter
from preschool_app import starter
from preschool_app.database import get_db



@starter.get("/")
async def index():
    pass
    return{"message": "Welcome to Preschool API"}
