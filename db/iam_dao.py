import uuid
from datetime import datetime, timedelta, timezone

from db.dao import Dao


class IamDao(Dao):

    def get_user_by_email(self, email):
        with self.db.cursor(dictionary=True) as cursor_user_from_email:
            sql = "SELECT * FROM bidding.user WHERE email = %s"
            cursor_user_from_email.execute(sql, (email.strip(),))
            return cursor_user_from_email.fetchone()

    def add_login(self, id_user, login_token, refresh_token):
        expire_token = datetime.now(timezone.utc) + timedelta(minutes=15)
        expire_refresh_token = datetime.now(timezone.utc) + timedelta(days=30)
        with self.db.cursor(dictionary=True) as cursor_login:
            sql = "INSERT INTO bidding.login (id, token, refresh_token, created_at, token_valid_until, refresh_token_valid_until, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (str(uuid.uuid4()), login_token, refresh_token, datetime.now(timezone.utc), expire_token, expire_refresh_token, id_user)
            cursor_login.execute(sql, val)
            self.db.commit()

    def expire_old_logins(self, id_user):
        with self.db.cursor(dictionary=True) as cursor_old_login:
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

    def get_user_by_access_token(self, access_token):
        with self.db.cursor(dictionary=True) as cursor_user_by_access_token:
            sql = "SELECT l.*, u.role FROM bidding.login l LEFT JOIN bidding.user u ON l.user_id = u.id WHERE l.token = %s"
            cursor_user_by_access_token.execute(sql, (access_token.strip(),))
            return cursor_user_by_access_token.fetchone()

    def get_all_users(self):
        with self.db.cursor(dictionary=True) as cursor_all_users:
            sql = "SELECT * FROM bidding.user WHERE role != 'AD' ORDER BY name"
            cursor_all_users.execute(sql)
            return cursor_all_users.fetchall()

    def get_user_by_id(self, user_id):
        with self.db.cursor(dictionary=True) as cursor_user_by_id:
            sql = "SELECT * FROM bidding.user WHERE id = %s AND role != 'AD'"
            cursor_user_by_id.execute(sql, (user_id.strip(),))
            return cursor_user_by_id.fetchone()

    def create_user(self, user_id, user_data):
        with self.db.cursor(dictionary=True) as cursor_create_user:
            sql = "INSERT INTO bidding.user (id, name, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (user_id, user_data.name, user_data.email, user_data.password, user_data.role, datetime.now(timezone.utc))
            cursor_create_user.execute(sql, val)
            self.db.commit()
