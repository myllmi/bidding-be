import uuid
from datetime import datetime, timezone

from db.dao import Dao


class UserDao(Dao):
    def get_user_by_email(self, email):
        with self.db.cursor(dictionary=True) as cursor_user_from_email:
            sql = "SELECT * FROM bidding.user WHERE email = %s"
            cursor_user_from_email.execute(sql, (email.strip(),))
            return cursor_user_from_email.fetchone()

    def get_user_by_access_token(self, access_token):
        with self.db.cursor(dictionary=True) as cursor_user_by_access_token:
            sql = "SELECT * FROM bidding.login l LEFT JOIN bidding.user u ON l.user_id = u.id WHERE l.token = %s"
            cursor_user_by_access_token.execute(sql, (access_token.strip(),))
            return cursor_user_by_access_token.fetchone()

    def get_all_users(self):
        with self.db.cursor(dictionary=True) as cursor_all_users:
            sql = "SELECT * FROM bidding.user WHERE role != 'AD' AND expired_at is null ORDER BY name"
            cursor_all_users.execute(sql)
            return cursor_all_users.fetchall()

    def get_user_by_id(self, user_id):
        with self.db.cursor(dictionary=True) as cursor_user_by_id:
            sql = "SELECT * FROM bidding.user WHERE id = %s AND role != 'AD' AND expired_at is null"
            cursor_user_by_id.execute(sql, (user_id.strip(),))
            return cursor_user_by_id.fetchone()

    def create_user(self, user_id, user_data):
        with self.db.cursor() as cursor_create_user:
            sql = "INSERT INTO bidding.user (id, name, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (user_id, user_data.name, user_data.email, user_data.password, user_data.role,
                   datetime.now(timezone.utc))
            cursor_create_user.execute(sql, val)
            self.db.commit()

    def update_user_by_id(self, user_id, user_data):
        with self.db.cursor() as cursor_update_user:
            sql = "UPDATE bidding.user SET name = %s, email = %s, role = %s WHERE id = %s"
            val = (user_data.name, user_data.email, user_data.role, user_id)
            cursor_update_user.execute(sql, val)
            self.db.commit()

    def delete_user_by_id(self, user_id):
        with self.db.cursor() as cursor_delete_user:
            sql = "UPDATE bidding.user SET expired_at = CURRENT_TIMESTAMP WHERE id = %s"
            val = (user_id.strip(),)
            cursor_delete_user.execute(sql, val)
            self.db.commit()

    def delete_user_sector(self, user_id):
        with self.db.cursor(dictionary=True) as cursor_delete_user_sector:
            sql = "DELETE FROM bidding.user_business_sector WHERE user_id = %s"
            val = (user_id.strip(),)
            cursor_delete_user_sector.execute(sql, val)
            self.db.commit()

    def add_user_sector(self, user_id, id_sector):
        with self.db.cursor() as cursor_add_user_sector:
            sql = "INSERT INTO bidding.user_business_sector (id, user_id, business_sector_id) VALUES (%s, %s, %s)"
            val = (str(uuid.uuid4()), user_id.strip(), id_sector.strip())
            cursor_add_user_sector.execute(sql, val)
            self.db.commit()
