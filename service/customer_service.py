from db.customer_dao import CustomerDao
from service.iam_service import IamService
from service.sector_service import SectorService


class CustomerService:
    def __init__(self):
        self.db = CustomerDao()
        self.iam_service = IamService()
        self.sector_service = SectorService()

    def list_customer_by_token(self, bearer_token: str):
        dict_user = self.iam_service.get_user_by_bearer_token(bearer_token)
        list_sector = self.sector_service.get_sector_by_user_id(dict_user['id'])
        arr_sector = [item['business_sector_id'] for item in list_sector]
        return self.db.get_customer_by_sector(arr_sector)
