from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, auth, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

import psycopg2
from psycopg2.extras import RealDictCursor
try: 
    conn = psycopg2.connect(host = 'localhost',database = 'fastapi', 
                            user = 'mysql', password = "",
                            cursor_factory = RealDictCursor)    # it is used to show the column in the database
    cursor = conn.cursor()
    print("Database connection established")

except Exception as error:
    print("Connection error")
   # print("Error:" error)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup", response_model=schemas.Token)
def signup(signup_data: schemas.Signup, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, signup_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db, signup_data)
    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=schemas.Token)
def login(login_data: schemas.Login, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_data)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/addPost", response_model=schemas.Post)
def add_post(
    post_data: schemas.AddPost,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    post = crud.create_post(db, post_data, current_user)
    return post

@app.get("/getPosts", response_model=list[schemas.Post])
def get_posts(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    posts = crud.get_user_posts(db, current_user.id)
    return posts

@app.delete("/deletePost", response_model=schemas.Post)
def delete_post(
    post_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    post = crud.delete_post(db, post_id, current_user.id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
