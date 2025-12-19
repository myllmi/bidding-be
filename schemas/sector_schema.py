from pydantic import BaseModel


class SectorModel(BaseModel):
    id: str | None = None
    sector_name: str