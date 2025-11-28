from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.database import get_session
from app.services import user_service


SessionDep = Annotated[Session, Depends(get_session)]

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with the provided information.",
)
def register_user(user: UserCreate, db: SessionDep):
    return user_service.create_user(db, user)


@user_router.get(
    "/",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    summary="List all users",
    description="Retrieve a list of all users in the system.",
)
def list_all_users(db: SessionDep):
    return user_service.get_all_users(db)


@user_router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieve a single user by their unique user ID.",
)
def get_user_by_id(user_id: int, db: SessionDep):
    return user_service.get_user_by_id(db, user_id)


@user_router.put(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update user",
    description="Update an existing user with new field values.",
)
def update_user(user_id: int, data: UserUpdate, db: SessionDep):
    return user_service.update_user(db, user_id, data)


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Soft-delete a user by setting the 'is_active' flag to False.",
)
def delete_user(user_id: int, db: SessionDep):
    return user_service.delete_user(db, user_id)
