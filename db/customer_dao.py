from db.dao import Dao


class CustomerDao(Dao):
    def get_customer_by_sector(self, list_sector):
        if not list_sector:
            # Prevent invalid SQL: IN ()
            sql = "SELECT * FROM customer WHERE 1 = 0"
        else:
            placeholders = ", ".join(["%s"] * len(list_sector))
            sql = f"SELECT * FROM customer WHERE business_sector_id IN ({placeholders})"
        with self.db.cursor(dictionary=True) as cursor_customer_by_sector:
            cursor_customer_by_sector.execute(sql, list_sector)
            return cursor_customer_by_sector.fetchall()
