from datetime import timezone, datetime

from db.dao import Dao


class SectorDao(Dao):
    def get_all_sector(self):
        with self.db.cursor(dictionary=True) as cursor_all_sector:
            sql = "SELECT * FROM bidding.business_sector WHERE expired_at is null ORDER BY sector_name DESC"
            cursor_all_sector.execute(sql)
            return cursor_all_sector.fetchall()

    def get_sector_by_id(self, sector_id):
        with self.db.cursor(dictionary=True) as cursor_sector_by_id:
            sql = "SELECT * FROM bidding.business_sector WHERE id = %s"
            cursor_sector_by_id.execute(sql, (sector_id,))
            return cursor_sector_by_id.fetchone()

    def update_sector_by_id(self, sector_id, sector):
        with self.db.cursor() as cursor_update_sector_by_id:
            sql = "UPDATE bidding.business_sector SET sector_name = %s WHERE id = %s"
            cursor_update_sector_by_id.execute(sql, (sector.sector_name, sector_id))
            self.db.commit()

    def delete_sector_by_id(self, sector_id):
        with self.db.cursor() as cursor_delete_sector_by_id:
            sql = "UPDATE bidding.business_sector SET expired_at = CURRENT_TIMESTAMP WHERE id = %s"
            cursor_delete_sector_by_id.execute(sql, (sector_id,))
            self.db.commit()

    def get_sector_by_name(self, sector_name):
        with self.db.cursor(dictionary=True) as cursor_sector_by_name:
            sql = "SELECT * FROM bidding.business_sector WHERE sector_name = %s"
            cursor_sector_by_name.execute(sql, (sector_name,))
            return cursor_sector_by_name.fetchall()

    def create_sector(self, sector_id, sector):
        with self.db.cursor() as cursor_create_sector:
            sql = "INSERT INTO bidding.business_sector (id, sector_name, created_at) VALUES (%s, %s, %s)"
            cursor_create_sector.execute(sql, (sector_id, sector.sector_name, datetime.now(timezone.utc)))
            self.db.commit()

    def get_sector_by_user_id(self, user_id):
        with self.db.cursor(dictionary=True) as cursor_sector_by_user_id:
            sql = "SELECT * FROM bidding.user_business_sector ubs LEFT JOIN bidding.business_sector bs ON ubs.business_sector_id = bs.id WHERE user_id = %s AND bs.expired_at is null"
            cursor_sector_by_user_id.execute(sql, (user_id,))
            return cursor_sector_by_user_id.fetchall()
