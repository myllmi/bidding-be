from typing import List

from fastapi import APIRouter

from schemas.sector_schema import SectorModel
from service.sector_service import SectorService

router = APIRouter()


@router.get("/list",
            response_model=List[SectorModel],
            summary="List all business sectors",
            description="List all business sectors")
def list_business_sectors():
    sector_service = SectorService()
    return sector_service.get_all_sectors()


@router.get("/{sector_id}",
            response_model=SectorModel,
            summary="Get a business sector",
            description="Get a business sector")
def get_business_sector(sector_id: str):
    sector_service = SectorService()
    return sector_service.get_sector_by_id(sector_id)


@router.post("",
             summary="Create a new business sector",
             description="Create a new business sector")
def create_business_sector(sector: SectorModel):
    sector_service = SectorService()
    return sector_service.create_sector(sector)


@router.put("/{sector_id}",
            response_model=SectorModel,
            summary="Update a business sector",
            description="Update a business sector")
def update_business_sector(sector_id: str, sector: SectorModel):
    sector_service = SectorService()
    return sector_service.update_sector_by_id(sector_id, sector)


@router.delete("/{sector_id}",
               summary="Delete a business sector",
               description="Delete a business sector")
def delete_business_sector(sector_id: str):
    sector_service = SectorService()
    sector_service.delete_sector_by_id(sector_id)
    return {}
