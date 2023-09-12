from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class Signup(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class AddPost(BaseModel):
    text: str

class Post(BaseModel):
    id: int
    text: str
    owner_id: int
