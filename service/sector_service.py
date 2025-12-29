import uuid

from db.sector_dao import SectorDao
from exception.business_exception import BusinessException
from service.iam_service import IamService
from util.constant import ROLE_ADMIN


class SectorService:
    def __init__(self):
        self.db = SectorDao()

    def list_sector(self, dict_user):
        if dict_user['role'] != ROLE_ADMIN:
            list_sector = self.get_sector_by_user_id(dict_user['id'])
            return list_sector
        else:
            return self.db.get_all_sector()

    def get_sector_by_id(self, sector_id):
        dict_sector = self.db.get_sector_by_id(sector_id)
        if dict_sector is None:
            raise BusinessException("Business Sector not found", 404)
        return dict_sector

    def create_sector(self, sector_data):
        list_sector = self.db.get_sector_by_name(sector_data.sector_name)
        if len(list_sector) > 0:
            raise BusinessException(f"Business Sector exists ({len(list_sector)})", 409)
        sector_id = str(uuid.uuid4())
        self.db.create_sector(sector_id, sector_data)
        return {
            "id": sector_id,
            "sector_name": sector_data.sector_name,
        }

    def update_sector_by_id(self, sector_id, sector_data):
        dict_sector = self.db.get_sector_by_id(sector_id)
        if dict_sector is None:
            raise BusinessException("Business Sector not found", 404)
        if dict_sector["expired_at"] is not None:
            raise BusinessException("Invalid Business Sector", 409)
        self.db.update_sector_by_id(sector_id, sector_data)
        return {
            "id": sector_id,
            "sector_name": sector_data.sector_name,
        }

    def delete_sector_by_id(self, sector_id):
        dict_sector = self.db.get_sector_by_id(sector_id)
        if dict_sector is None:
            raise BusinessException("Business Sector not found", 404)
        if dict_sector["expired_at"] is not None:
            raise BusinessException("Invalid Business Sector", 409)
        # TODO: Check if sector has customers and tenders
        self.db.delete_sector_by_id(sector_id)

    def get_sector_by_user_id(self, user_id):
        return self.db.get_sector_by_user_id(user_id)
