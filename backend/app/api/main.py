from app.api.routes import auth_router
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
