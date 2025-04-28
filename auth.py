from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from models import UserRead,User
from db_manager import DatabaseManager
from connect_db import ConnectDB

class Auth:
    def __init__(self, SECRET_KEY, ALGORITHM, pwd_context, oauth2_schema) -> None:
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.pwd_context = pwd_context
        self.oauth2_schema = oauth2_schema

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user(self, email: str) -> Union[UserRead, bool]:

        connect_db = ConnectDB()
        conn = connect_db.get_connection()

        db_manager = DatabaseManager()
        user = db_manager.read_user_record_by_email(
            conn, email
        )

        return user

    def authenticate_user(self, email: str, password: str) -> Union[User, bool]:
        user = self.get_user(email=email)

        if not user:
            return False
        if not self.verify_password(password,user.hashed_password):
            return False
        return user


    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
