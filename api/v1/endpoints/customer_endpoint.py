from typing import List, Optional

from fastapi import APIRouter, Depends, Header

from filter.request_filter import check_access_token
from schemas.customer_schema import CustomerModelRes
from service.customer_service import CustomerService
from util.helper import get_current_token

router = APIRouter()


@router.get("/list",
            response_model=List[CustomerModelRes],
            summary="List all customers by user",
            description="List all customers by user",
            dependencies=[Depends(check_access_token)])
def list_customers_by_token(bearer_token: str = Depends(get_current_token), customer_service: CustomerService = Depends(CustomerService)):
    print(customer_service.list_customer_by_token(bearer_token))
    return []
