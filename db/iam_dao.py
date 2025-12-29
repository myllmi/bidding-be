import uuid
from datetime import datetime, timedelta, timezone

from db.dao import Dao


class IamDao(Dao):
    def add_login(self, id_user, login_token, refresh_token):
        expire_token = datetime.now(timezone.utc) + timedelta(minutes=15)
        expire_refresh_token = datetime.now(timezone.utc) + timedelta(days=30)
        with self.db.cursor() as cursor_login:
            sql = "INSERT INTO bidding.login (id, token, refresh_token, created_at, token_valid_until, refresh_token_valid_until, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (str(uuid.uuid4()), login_token, refresh_token, datetime.now(timezone.utc), expire_token,
                   expire_refresh_token, id_user)
            cursor_login.execute(sql, val)
            self.db.commit()

    def expire_old_logins(self, id_user):
        with self.db.cursor() as cursor_old_login:
            sql = "UPDATE bidding.login SET expired_at = %s WHERE user_id = %s AND expired_at is null"
            val = (datetime.now(timezone.utc), id_user)
            cursor_old_login.execute(sql, val)
            self.db.commit()

    def get_login_by_refresh_token(self, refresh_token):
        with self.db.cursor(dictionary=True) as cursor_login_by_refresh_token:
            sql = "SELECT * FROM bidding.login WHERE refresh_token = %s"
            cursor_login_by_refresh_token.execute(sql, (refresh_token.strip(),))
            return cursor_login_by_refresh_token.fetchone()

    def get_login_by_access_token(self, access_token):
        with self.db.cursor(dictionary=True) as cursor_login_by_access_token:
            sql = "SELECT * FROM bidding.login WHERE login.token = %s"
            cursor_login_by_access_token.execute(sql, (access_token.strip(),))
            return cursor_login_by_access_token.fetchone()
