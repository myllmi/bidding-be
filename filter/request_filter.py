from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from exception.security_exception import SecurityException
from service.iam_service import IamService
from service.user_service import UserService
from util.constant import ROLE_ADMIN, ROLE_ANALYST, ROLE_MANAGER

security = HTTPBearer()


def check_access_token(credentials: HTTPAuthorizationCredentials = Depends(security),
                       iam_service: IamService = Depends(IamService)):
    check_bearer(credentials)
    iam_service.check_access_token(credentials.credentials)


def check_admin_role(credentials: HTTPAuthorizationCredentials = Depends(security),
                     user_service: UserService = Depends(UserService)):
    check_bearer(credentials)
    user_service.check_admin_role(credentials.credentials, ROLE_ADMIN)


def check_analyst_role(credentials: HTTPAuthorizationCredentials = Depends(security),
                       user_service: UserService = Depends(UserService)):
    check_bearer(credentials)
    user_service.check_admin_role(credentials.credentials, ROLE_ANALYST)


def check_manager_role(credentials: HTTPAuthorizationCredentials = Depends(security),
                       user_service: UserService = Depends(UserService)):
    check_bearer(credentials)
    user_service.check_admin_role(credentials.credentials, ROLE_MANAGER)


def check_bearer(credentials: HTTPAuthorizationCredentials):
    if credentials.scheme.upper() != "BEARER":
        raise SecurityException("Invalid credentials", 401)
