from typing import List

from schemas.camel_schema import CamelModelBase


class UserModelbase(CamelModelBase):
    email: str
    name: str
    role: str
    list_id_sector: List[str] = []


class UserModelRes(UserModelbase):
    id: str


class UserModelReq(UserModelbase):
    id: str | None = None
    password: str | None = None
