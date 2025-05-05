from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from models import AdminRegister
import datetime
from config import SECRET_KEY, ALGORITHM
from database import *

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Special Admin Registration Code
ADMIN_SECRET_CODE = "SSVM1983"

def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    data.update({"exp": expiration})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
@router.post("/register")
def admin_register(admin: AdminRegister):
    if admin.secret_code != ADMIN_SECRET_CODE:
        raise HTTPException(status_code=403, detail="Invalid admin code")

    if admins_collection.find_one({"email": admin.email}):
        raise HTTPException(status_code=400, detail="Admin already registered")

    hashed_password = pwd_context.hash(admin.password)
    admins_collection.insert_one({
        "name": admin.name, 
        "email": admin.email, 
        "password": hashed_password
    })

    return {"message": "Admin registered successfully!"}


@router.post("/login")  #  The route should be "/login", NOT "/admin/login"
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = admins_collection.find_one({"email": form_data.username})
    if not admin or not pwd_context.verify(form_data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({"sub": admin["email"], "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "message": "Admin login successful","role":"admin"}
