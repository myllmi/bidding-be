from pydantic import BaseModel


class SectorModelReq(BaseModel):
    id: str | None = None
    sector_name: str


class SectorModelRes(BaseModel):
    id: str
    sector_name: str
