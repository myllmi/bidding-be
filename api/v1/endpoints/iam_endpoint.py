from fastapi import APIRouter, Response, Cookie, Depends

from exception.security_exception import SecurityException
from filter.request_filter import check_access_token
from schemas.iam_schema import LoginModelReq
from service.iam_service import IamService

router = APIRouter()


@router.post("/login",
             summary="Login",
             description="Login")
def login(data: LoginModelReq, response: Response):  # , pub_service: PubService = Depends()
    iam_service = IamService()
    tokens = iam_service.login_user(data.email, data.password)
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
def refresh_access_token(response: Response, refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise SecurityException("Missing refresh token", 401)
    iam_service = IamService()
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


@router.get("/user/list",
            summary="List Users",
            description="List Users",
            dependencies=[Depends(check_access_token)])
def list_users(iam_service: IamService = Depends(IamService)):
    return iam_service.get_all_users()


@router.get("/user/{user_id}",
            summary="Get Users by ID",
            description="Get Users by ID",
            dependencies=[Depends(check_access_token)])
def list_users(user_id: str, iam_service: IamService = Depends(IamService)):
    return iam_service.get_user_by_id(user_id)
