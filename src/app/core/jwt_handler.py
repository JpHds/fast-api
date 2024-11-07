from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from src.app.core.config import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.app.core.hashing import verify_password
from src.app.models.admin_model import Admin
from src.app.models.superadmin_model import SuperAdmin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="security/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_super_admin_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload


def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only administrators are allowed to access this resource."
        )
    return current_user


def is_super_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only super admins are allowed to access this resource."
        )
    return current_user


def is_admin_or_super_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only admins and super admins are allowed to access this resource."
        )
    return current_user


def authenticate_admin(db: Session, username: str, password: str) -> Optional[Admin]:
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin and verify_password(password, admin.password):
        return admin
    return None


def authenticate_super_admin(db: Session, username: str, password: str) -> Optional[SuperAdmin]:
    super_admin = db.query(SuperAdmin).filter(SuperAdmin.username == username).first()
    if super_admin and verify_password(password, super_admin.password):
        return super_admin
    return None
