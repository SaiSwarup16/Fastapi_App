from sqlalchemy.orm import Session
from . import models

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.Signup):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, login_data: schemas.Login):
    user = get_user_by_email(db, login_data.email)
    if not user or not auth.verify_password(login_data.password, user.hashed_password):
        return None
    return user

def create_post(db: Session, post_data: schemas.AddPost, current_user: models.User):
    db_post = models.Post(**post_data.dict(), owner_id=current_user.id)
