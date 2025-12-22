from pydantic import BaseModel, Field

class LoginModelReq(BaseModel):
    email: str
    password: str

class UserModelRes(BaseModel):
    id: str
    email: str
    name: str
    role: str

class UserModelReq(BaseModel):
    id: str | None = None
    email: str
    name: str
    password: str
    role: str