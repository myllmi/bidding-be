from datetime import datetime, timezone, date, time, timedelta
from decimal import Decimal

from db.iam_dao import IamDao
from exception.security_exception import SecurityException
from util.helper import gen_hash_512

def check_token(dict_login):
    if dict_login is None:
        raise SecurityException("Invalid access token", 401)
    if dict_login['expired_at'] is not None:
        raise SecurityException("Invalid token", 401)
    expires_at = dict_login['token_valid_until']
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        raise SecurityException("Token expired", 401)


class IamService:
    def __init__(self):
        self.ROLE_ADMIN = 'AD'
        self.ROLE_ANALYST = 'AN'
        self.ROLE_MANAGER = 'MG'
        self.db = IamDao()

    def create_login_token(self, id_user):
        login_token = gen_hash_512(id_user + datetime.now().strftime("%Y%m%d%H%M%S") + "ACCESS_TOKEN")
        refresh_token = gen_hash_512(id_user + datetime.now().strftime("%Y%m%d%H%M%S") + "REFRESH_TOKEN")
        self.db.expire_old_logins(id_user)
        self.db.add_login(id_user, login_token, refresh_token)
        return login_token, refresh_token

    def login_user(self, email, password):
        dict_user = self.db.get_user_by_email(email)
        if dict_user is None:
            raise SecurityException("Invalid login details", 401)
        if dict_user['expired_at'] is not None:
            raise SecurityException("User expired", 401)
        hashed_password = gen_hash_512(password)
        if dict_user['password'] != hashed_password:
            raise SecurityException("Invalid login details", 401)
        login_token, refresh_token = self.create_login_token(dict_user['id'])
        return {"access_token": login_token, "refresh_token": refresh_token}

    def refresh_access_token(self, refresh_token):
        dict_login = self.db.get_login_by_refresh_token(refresh_token)
        if dict_login is None:
            raise SecurityException("Invalid refresh token", 401)
        if dict_login['expired_at'] is not None:
            raise SecurityException("Invalid token", 401)
        expires_at = dict_login['refresh_token_valid_until']
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            raise SecurityException("Token expired", 401)
        login_token, refresh_token = self.create_login_token(dict_login['user_id'])
        return {"access_token": login_token, "refresh_token": refresh_token}

    def check_access_token(self, access_token):
        dict_login = self.db.get_login_by_access_token(access_token)
        check_token(dict_login)

    def check_admin_role(self, access_token, role):
        dict_user = self.db.get_user_by_access_token(access_token)
        check_token(dict_user)
        if dict_user['role'] != role:
            raise SecurityException("Permission denied", 403)
