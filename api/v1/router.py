from fastapi import APIRouter, Depends

from api.v1.endpoints import iam_endpoint, sector_endpoint
from filter.request_filter import check_access_token

api_router = APIRouter()

api_router.include_router(iam_endpoint.router, prefix="/iam")
api_router.include_router(sector_endpoint.router, prefix="/sector")
