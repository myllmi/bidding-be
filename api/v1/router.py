from fastapi import APIRouter, Depends

from api.v1.endpoints import iam, sector
from filter.request_filter import check_access_token

api_router = APIRouter()

api_router.include_router(iam.router, prefix="/iam")
api_router.include_router(sector.router, prefix="/sector", dependencies=[Depends(check_access_token)])
