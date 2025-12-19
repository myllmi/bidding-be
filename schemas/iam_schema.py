from pydantic import BaseModel, Field

class LoginModelReq(BaseModel):
    email: str
    password: str
