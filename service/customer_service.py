from db.customer_dao import CustomerDao
from util.constant import ROLE_ADMIN


class CustomerService:
    def __init__(self):
        self.db = CustomerDao()

    def list_customer(self, dict_user, list_sector):
        if dict_user['role'] != ROLE_ADMIN:
            arr_sector = [item['business_sector_id'] for item in list_sector]
            return self.db.get_customer_by_sector(arr_sector)
        else:
            return self.db.get_all_customer()