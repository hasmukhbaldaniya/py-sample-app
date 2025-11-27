from typing import List

from pydantic import BaseModel, constr, Field, EmailStr

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    first_name: constr(strip_whitespace=True, min_length=2, max_length=50) | None = Field(
        ..., description="First name must be 2–50 characters"
    )
    last_name: constr(strip_whitespace=True, min_length=2, max_length=50) | None = Field(
        ..., description="Last name must be 2–50 characters"
    )
    email: EmailStr = Field(
        ..., description="Must be a valid email address"
    )

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    first_name: constr(strip_whitespace=True, min_length=2, max_length=50) | None = Field(
        None, description="First name must be 2–50 characters"
    )
    last_name: constr(strip_whitespace=True, min_length=2, max_length=50) | None = Field(
        None, description="Last name must be 2–50 characters"
    )
    email: EmailStr | None = Field(
        None, description="Must be a valid email address"
    )

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class UserListResponse(BaseModel):
    count: int
    users: List[UserResponse]