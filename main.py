from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router
from exception.business_exception import BusinessException
from exception.security_exception import SecurityException

app = FastAPI(
    title="Bidding AI API",
    description="API for Bidding AI",
    version="0.1.0b",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular dev
        # "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],        # includes OPTIONS
    allow_headers=["*"],        # includes Authorization
)


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": "BUSINESS_ERROR",
            "message": exc.message,
            "code": exc.code,
        },
    )


@app.exception_handler(SecurityException)
async def security_exception_handler(request: Request, exc: SecurityException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": "SECURITY_ERROR",
            "message": exc.message,
            "code": exc.code,
        },
    )


app.include_router(api_router, prefix="/api/v1")
