from typing import List

from fastapi import APIRouter, Depends

from filter.request_filter import check_admin_role, check_access_token
from schemas.sector_schema import SectorModelRes, SectorModelReq
from service.iam_service import IamService
from service.sector_service import SectorService
from service.user_service import UserService
from util.helper import get_current_token

router = APIRouter()


@router.get("/list",
            response_model=List[SectorModelRes],
            summary="List all business sectors",
            description="List all business sectors",
            dependencies=[Depends(check_access_token)])
def list_business_sectors(bearer_token: str = Depends(get_current_token),
                          sector_service: SectorService = Depends(SectorService),
                          user_service: UserService = Depends(UserService)):
    dict_user = user_service.get_user_by_bearer_token(bearer_token)
    return sector_service.list_sector(dict_user)


@router.get("/{sector_id}",
            response_model=SectorModelRes,
            summary="Get a business sector",
            description="Get a business sector",
            dependencies=[Depends(check_access_token)])
def get_business_sector(sector_id: str, sector_service: SectorService = Depends(SectorService)):
    return sector_service.get_sector_by_id(sector_id)


@router.post("",
             response_model=SectorModelRes,
             summary="Create a new business sector",
             description="Create a new business sector",
             dependencies=[Depends(check_access_token), Depends(check_admin_role)])
def create_business_sector(sector_data: SectorModelReq, sector_service: SectorService = Depends(SectorService)):
    return sector_service.create_sector(sector_data)


@router.put("/{sector_id}",
            response_model=SectorModelRes,
            summary="Update a business sector",
            description="Update a business sector",
            dependencies=[Depends(check_access_token), Depends(check_admin_role)])
def update_business_sector(sector_id: str, sector_data: SectorModelReq,
                           sector_service: SectorService = Depends(SectorService)):
    return sector_service.update_sector_by_id(sector_id, sector_data)


@router.delete("/{sector_id}",
               summary="Delete a business sector",
               description="Delete a business sector",
               dependencies=[Depends(check_access_token), Depends(check_admin_role)])
def delete_business_sector(sector_id: str, sector_service: SectorService = Depends(SectorService)):
    sector_service.delete_sector_by_id(sector_id)
    return {}
