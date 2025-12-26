from fastapi import APIRouter

from api.v1.endpoints import iam_endpoint, sector_endpoint, project_endpoint, resume_endpoint, customer_endpoint

api_router = APIRouter()

api_router.include_router(iam_endpoint.router, prefix="/iam")
api_router.include_router(sector_endpoint.router, prefix="/sector")
api_router.include_router(project_endpoint.router, prefix="/project")
api_router.include_router(resume_endpoint.router, prefix="/resume")
api_router.include_router(customer_endpoint.router, prefix="/customer")
