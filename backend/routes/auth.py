from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import datetime
from models import UserRegister

from config import SECRET_KEY, ALGORITHM
from database import *

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    data.update({"exp": expiration})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(user: UserRegister):
    if user.class_level < 6 or user.class_level > 10:
        raise HTTPException(status_code=400, detail="Class must be between 6 and 10.")

    if students_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = pwd_context.hash(user.password)
    students_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "class_level": user.class_level,
    })

    return {"message": "Registration successful!"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    student = students_collection.find_one({"email": form_data.username})
    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": student["email"], "class_level": student["class_level"]}, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "name": student["name"],
        "email": student["email"],
        "class_level": student.get("class_level"),  #  Ensure class_level is returned
        "role1":"student" #additional
    }

