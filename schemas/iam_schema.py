from schemas.camel_schema import CamelModelBase


class LoginModelReq(CamelModelBase):
    email: str
    password: str
