from schemas.camel_schema import CamelModelBase


class SectorModelBase(CamelModelBase):
    sector_name: str


class SectorModelReq(SectorModelBase):
    id: str | None = None


class SectorModelRes(SectorModelBase):
    id: str
