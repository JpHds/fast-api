from typing import List

from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from src.app.core.dependencies import get_db
from src.app.core.jwt_handler import is_super_admin

from src.app.services.admin import AdminService

router = APIRouter()

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class AdminRequest(BaseModel):
    username: str
    email: str


@router.get("/list-admins", response_model=List[AdminResponse])
def list_admins(db: Session = Depends(get_db),
                 current_user: dict = Depends(is_super_admin)):
    return AdminService.get_all_admins(db)

@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin_by_id(admin_id: int, db: Session = Depends(get_db),
                     current_user: dict = Depends(is_super_admin)):
    return AdminService.get_admin_by_id(db, admin_id)

@router.put("/{admin_id}", response_model=AdminResponse)
def update_client_by_id(admin_id: int, admin_data: AdminRequest, db: Session = Depends(get_db),
                        current_user: dict = Depends(is_super_admin)):
    return AdminService.update_admin_by_id(db, admin_id, admin_data.dict())


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client_by_id(admin_id: int, db: Session = Depends(get_db),
                        current_user: dict = Depends(is_super_admin)):
    AdminService.delete_admin_by_id(db, admin_id)
