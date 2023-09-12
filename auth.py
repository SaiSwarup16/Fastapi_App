from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import models, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token has expired")

def get_current_user(token: str = Depends(oauth2_scheme), db: database.SessionLocal = Depends(database.get_db)):
    email = decode_token(token)
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
