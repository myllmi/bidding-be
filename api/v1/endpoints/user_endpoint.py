from typing import List

from fastapi import APIRouter, Depends

from exception.security_exception import SecurityException
from filter.request_filter import check_access_token, check_admin_role
from schemas.user_schema import UserModelRes, UserModelReq
from service.sector_service import SectorService
from service.user_service import UserService
from util.helper import get_current_token

router = APIRouter()


@router.get("/list",
            response_model=List[UserModelRes],
            summary="List Users by Role",
            description="List Users by Role",
            dependencies=[Depends(check_access_token)])
def list_users_by_role(bearer_token: str = Depends(get_current_token),
                       user_service: UserService = Depends(UserService),
                       sector_service: SectorService = Depends(SectorService)):
    dict_token = user_service.get_user_by_bearer_token(bearer_token)
    if dict_token is None:
        raise SecurityException("Invalid credentials", 401)
    list_sector = sector_service.get_sector_by_user_id(dict_token['user_id'])
    return user_service.get_all_users_by_role(dict_token, list_sector)


@router.get("/current",
            response_model=UserModelRes,
            summary="Get Users by ID",
            description="Get Users by ID",
            dependencies=[Depends(check_access_token)])
def get_current_user(bearer_token: str = Depends(get_current_token), user_service: UserService = Depends(UserService)):
    return user_service.get_current_user(bearer_token)


@router.get("/get/{user_id}",
            response_model=UserModelRes,
            summary="Get Users by ID",
            description="Get Users by ID",
            dependencies=[Depends(check_access_token)])
def get_user_by_id(user_id: str, bearer_token: str = Depends(get_current_token),
                   user_service: UserService = Depends(UserService),
                   sector_service: SectorService = Depends(SectorService)):
    dict_token = user_service.get_user_by_bearer_token(bearer_token)
    if dict_token is None:
        raise SecurityException("Invalid credentials", 401)
    first_list = sector_service.get_sector_by_user_id(dict_token['user_id'])
    second_list = sector_service.get_sector_by_user_id(user_id)
    return user_service.get_user_by_id(user_id, dict_token['role'], first_list, second_list)


@router.post("",
             response_model=UserModelRes,
             summary="Create User",
             description="Create User",
             dependencies=[Depends(check_access_token), Depends(check_admin_role)])
def create_user(user_data: UserModelReq, user_service: UserService = Depends(UserService)):
    return user_service.create_user(user_data)


@router.put("/{user_id}",
            response_model=UserModelRes,
            summary="Update User by ID",
            description="Update User by ID",
            dependencies=[Depends(check_access_token), Depends(check_admin_role)])
def update_user(user_id: str, user_data: UserModelReq, user_service: UserService = Depends(UserService)):
    return user_service.update_user(user_id, user_data)


@router.delete("/{user_id}",
               summary="Delete User by ID",
               description="Delete User by ID",
               dependencies=[Depends(check_access_token), Depends(check_admin_role)])
def delete_user(user_id: str, user_service: UserService = Depends(UserService)):
    user_service.delete_user(user_id)
    return {}
