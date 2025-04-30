from fastapi import APIRouter, Depends,HTTPException
from auth import Auth
from models import User,UserAddForm,UserReadAll
from typing import List
from models import Message
from connect_db import ConnectDB
from db_manager import DatabaseManager
from fastapi.responses import JSONResponse
from routes.auth_routes import get_current_active_user
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


auth = Auth(
    SECRET_KEY=SECRET_KEY,
    ALGORITHM=ALGORITHM,
    pwd_context=pwd_context,
    oauth2_schema=oauth2_schema
)

# all_user
@router.get("/",response_model=List[UserReadAll])
async def all_users(current_user: User = Depends(get_current_active_user)):

    connect_db = ConnectDB()
    conn = connect_db.get_connection()
    db_manager = DatabaseManager()
    users = db_manager.read_all_user_record(conn)

    if not users:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for the user."
        )

    return users


# detail_user
@router.get("/{user_id}",response_model=User)
async def user(user_id,current_user: User = Depends(get_current_active_user)):

    connect_db = ConnectDB()
    conn = connect_db.get_connection()
    db_manager = DatabaseManager()
    user = db_manager.read_user_record_by_id(conn, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for the user."
        )

    return user



# add_user
# async def create_user(form_data:UserForm):
@router.post("/", response_model=Message)
async def create_user(form_data:UserAddForm,current_user: User = Depends(get_current_active_user)):
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()


        db_manager = DatabaseManager()
        message = db_manager.create_user_record(
            conn=conn,
            username=form_data.username,
            full_name=form_data.full_name,
            hashed_password=auth.get_password_hash(form_data.password),
            email=form_data.email,
            is_manager=form_data.is_manager
        )
        return message

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

# edit_user
@router.put("/{user_id}", response_model=Message)
async def update_user(user_id,form_data:User,current_user: User = Depends(get_current_active_user)):
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()

        db_manager = DatabaseManager()
        message = db_manager.update_user_record(
            conn=conn,
            user_id=user_id,
            username=form_data.username,
            full_name=form_data.full_name,
            email=form_data.email,
            is_manager=form_data.is_manager,
            disabled=form_data.disabled
        )
        return message

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

# delete_user
@router.delete("/{user_id}", response_model=Message)
async def delete_user(user_id,current_user: User = Depends(get_current_active_user)):
    try:
        connect_db = ConnectDB()
        conn = connect_db.get_connection()
        db_manager = DatabaseManager()
        message = db_manager.delete_user_record(
            conn=conn,
            id=user_id,
        )
        return message

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {str(e)}"}
        )

