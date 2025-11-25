from fastapi import APIRouter

user_router = APIRouter(prefix="/user")

@user_router.get("/")
def list_users():
    return {"message": "Hello World"}