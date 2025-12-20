from fastapi import Header, APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from exception.security_exception import SecurityException
from service.iam_service import IamService

security = HTTPBearer()


def check_access_token(credentials: HTTPAuthorizationCredentials = Depends(security), iam_service: IamService = Depends(IamService)):
    if credentials.scheme.upper() != "BEARER":
        raise SecurityException("Invalid credentials", 401)
    iam_service.check_access_token(credentials.credentials)


def check_admin_role(credentials: HTTPAuthorizationCredentials = Depends(security), iam_service: IamService = Depends(IamService)):
    if credentials.scheme.upper() != "BEARER":
        raise SecurityException("Invalid credentials", 401)
    iam_service.check_admin_role(credentials.credentials)
