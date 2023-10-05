import os
from preschool_app import starter, engine, Base
from instance.config import SECRET_KEY, DATABASE_URI

os.environ["SECRET_KEY"] = os.getenv("SECRET_KEY", SECRET_KEY)
os.environ["DATABASE_URI"] = os.getenv("DATABASE_URI", DATABASE_URI)

Base.metadata.create_all(bind = engine)
print("Server running on port 8000")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(starter)