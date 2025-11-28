from typing import Optional

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "janedoe",
                "email": "jane@example.com",
                "full_name": "Jane Doe",
            }
        }


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "newusername",
                "email": "newemail@example.com",
                "is_active": True,
            }
        }


class UserRead(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "created_at": "2025-01-01T12:00:00Z",
                "is_active": True,
            }
        }
