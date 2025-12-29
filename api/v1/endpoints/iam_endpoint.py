from fastapi import APIRouter, Response, Cookie, Depends

from exception.security_exception import SecurityException
from schemas.iam_schema import LoginModelReq
from service.iam_service import IamService
from service.user_service import UserService

router = APIRouter()


@router.post("/login",
             summary="Login",
             description="Login")
def login(data: LoginModelReq, response: Response, iam_service: IamService = Depends(IamService), user_service: UserService = Depends(UserService)):
    dict_user = user_service.get_user_by_email(data.email)
    print(dict_user)
    tokens = iam_service.login_user(data.email, data.password, dict_user)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        # secure=True,  # required in production (HTTPS)
        samesite="lax",  # or "strict" / "none"
        max_age=30 * 24 * 60 * 60,  # 14 days (seconds)
        path="/"
    )
    return {"token": tokens["access_token"]}


@router.get("/refresh",
            summary="Refresh Access Token",
            description="Refresh Access Token"
            )
def refresh_access_token(response: Response, refresh_token: str | None = Cookie(default=None),
                         iam_service: IamService = Depends(IamService)):
    if not refresh_token:
        raise SecurityException("Missing refresh token", 401)
    tokens = iam_service.refresh_access_token(refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        # secure=True,  # required in production (HTTPS)
        samesite="lax",  # or "strict" / "none"
        max_age=30 * 24 * 60 * 60,  # 14 days (seconds)
        path="/"
    )
    return {"token": tokens["access_token"]}
