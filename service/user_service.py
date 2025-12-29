import uuid

from db.user_dao import UserDao
from exception.business_exception import BusinessException
from exception.security_exception import SecurityException
from util.constant import ROLE_ADMIN
from util.helper import gen_hash_512, check_same_sector, check_token


class UserService:
    def __init__(self):
        self.db = UserDao()

    def create_user(self, user_data):
        list_user = self.db.get_user_by_email(user_data.email)
        if list_user is not None:
            raise BusinessException("User exists, check the email", 409)
        user_id = str(uuid.uuid4())
        user_data.password = gen_hash_512(user_data.password)
        self.db.create_user(user_id, user_data)
        self.refresh_user_sector(user_id, user_data.list_id_sector)
        return {
            "id": user_id,
            "email": user_data.email,
            "name": user_data.name,
            "role": user_data.role,
            "list_id_sector": user_data.list_id_sector,
        }

    def update_user(self, user_id, user_data):
        dict_user = self.db.get_user_by_id(user_id)
        if dict_user is None:
            raise BusinessException("User not found", 404)
        if dict_user["expired_at"] is not None:
            raise BusinessException("Invalid User", 409)
        self.db.update_user_by_id(user_id, user_data)
        self.refresh_user_sector(user_id, user_data.list_id_sector)
        return {
            "id": user_id,
            "email": user_data.email,
            "name": user_data.name,
            "role": user_data.role,
            "list_id_sector": user_data.list_id_sector,
        }

    def delete_user(self, user_id):
        dict_user = self.db.get_user_by_id(user_id)
        if dict_user is None:
            raise BusinessException("User not found", 404)
        if dict_user["expired_at"] is not None:
            raise BusinessException("Invalid User", 409)
        if dict_user["role"] == "AD":
            raise BusinessException("Admin user can't be deleted!", 409)
        # TODO: Check if user has tender
        self.db.delete_user_by_id(user_id)

    def refresh_user_sector(self, user_id, list_id_sector):
        self.db.delete_user_sector(user_id)
        for id_sector in list_id_sector:
            self.db.add_user_sector(user_id, id_sector)

    def get_user_by_bearer_token(self, token):
        dict_user = self.db.get_user_by_access_token(token)
        if dict_user is None:
            raise SecurityException("Invalid credentials", 401)
        return dict_user

    def get_all_users_by_role(self, bearer_token):
        return []

    def get_current_user(self, bearer_token):
        return {}

    def get_user_by_email(self, email):
        dict_user = self.db.get_user_by_email(email)
        if dict_user is None:
            raise BusinessException("User not found", 404)
        return dict_user

    def get_user_by_id(self, user_id, bearer_token):
        dict_token = self.db.get_user_by_access_token(bearer_token)
        if dict_token is None:
            raise SecurityException("Invalid credentials", 401)
        dict_user = self.db.get_user_by_id(user_id)
        if dict_token['role'] != ROLE_ADMIN:
            if not check_same_sector(dict_token['user_id'], dict_user['id']):
                dict_user = None
        if dict_user is None:
            raise BusinessException("User not found", 404)
        return dict_user

    def check_admin_role(self, access_token, role):
        dict_user = self.db.get_user_by_access_token(access_token)
        check_token(dict_user)
        if dict_user['role'] != role:
            raise SecurityException("Permission denied", 403)
