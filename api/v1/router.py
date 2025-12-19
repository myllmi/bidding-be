from fastapi import APIRouter

from api.v1.endpoints import iam, sector

api_router = APIRouter()

api_router.include_router(iam.router, prefix="/iam")
api_router.include_router(sector.router, prefix="/sector")
