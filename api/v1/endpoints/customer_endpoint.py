from typing import List

from fastapi import APIRouter, Depends

from filter.request_filter import check_access_token
from schemas.customer_schema import CustomerModelRes
from service.customer_service import CustomerService
from service.sector_service import SectorService
from service.user_service import UserService
from util.helper import get_current_token

router = APIRouter()


@router.get("/list",
            response_model=List[CustomerModelRes],
            summary="List all customers by user",
            description="List all customers by user",
            dependencies=[Depends(check_access_token)])
def list_customers(bearer_token: str = Depends(get_current_token),
                   customer_service: CustomerService = Depends(CustomerService),
                   user_service: UserService = Depends(UserService),
                   sector_service: SectorService = Depends(SectorService)):
    dict_user = user_service.get_user_by_bearer_token(bearer_token)
    list_sector = sector_service.get_sector_by_user_id(dict_user['id'])
    return customer_service.list_customer(dict_user, list_sector)
