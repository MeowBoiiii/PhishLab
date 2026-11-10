from fastapi import APIRouter
from app.api.v1.endpoints import auth, campaigns, tracking

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autoryzacja"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Kampanie"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])

