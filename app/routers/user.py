from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.client import DBClient
from app.db.models.users import Users

user_router = APIRouter(prefix="/user")


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    first_name: str
    last_name: str
    email: str


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


@user_router.get("/")
def list_users(db: Session = Depends(DBClient.get_db_session)):
    """
    Get all users from the database.
    """
    users = db.query(Users).all()
    return {
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            for user in users
        ],
    }


@user_router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(DBClient.get_db_session)):
    """
    Get a specific user by ID.
    """
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }


@user_router.post("/", status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(DBClient.get_db_session)):
    """
    Create a new user in the database.
    """
    # Check if user with this email already exists
    existing_user = db.query(Users).filter(Users.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Create new user
    new_user = Users(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
        },
    }



@user_router.put("/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(DBClient.get_db_session)
):
    """
    Update an existing user by ID.
    """
    # Find the user
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if email is being updated and if it already exists
    if user_data.email and user_data.email != user.email:
        existing_user = db.query(Users).filter(Users.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

    # Update only the fields that are provided
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.email is not None:
        user.email = user_data.email

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    }




@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(DBClient.get_db_session)):
    """
    Delete a user by ID.
    """
    # Find the user
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Store user info before deletion for response
    deleted_user_info = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }

    # Delete the user
    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "deleted_user": deleted_user_info,
    }
