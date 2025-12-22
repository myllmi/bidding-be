from fastapi import APIRouter

from api.v1.endpoints import iam_endpoint, sector_endpoint

api_router = APIRouter()

api_router.include_router(iam_endpoint.router, prefix="/iam")
api_router.include_router(sector_endpoint.router, prefix="/sector")
