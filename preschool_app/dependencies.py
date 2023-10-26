from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from preschool_app.database import SessionLocal
from preschool_app import models  # Add this line to import your models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_user = db.query(models.User).filter(models.User.user_email == email).first()
    if db_user is None:
        raise credentials_exception

    return db_user
