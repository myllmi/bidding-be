from db.dao import Dao


class CustomerDao(Dao):
    def get_customer_by_sector(self, list_sector):
        if not list_sector:
            # Prevent invalid SQL: IN ()
            sql = "SELECT * FROM customer WHERE 1 = 0"
        else:
            placeholders = ", ".join(["%s"] * len(list_sector))
            sql = (f"SELECT c.*, bs.sector_name FROM bidding.customer c LEFT JOIN bidding.business_sector bs ON c.business_sector_id = bs.id "
                   f"WHERE c.expired_at IS NULL AND business_sector_id IN ({placeholders})")
        with self.db.cursor(dictionary=True) as cursor_customer_by_sector:
            cursor_customer_by_sector.execute(sql, list_sector)
            return cursor_customer_by_sector.fetchall()

    def get_all_customer(self):
        with self.db.cursor(dictionary=True) as cursor_customer:
            cursor_customer.execute("SELECT c.*, bs.sector_name FROM bidding.customer c LEFT JOIN bidding.business_sector bs ON c.business_sector_id = bs.id "
                                    "WHERE c.expired_at IS NULL ORDER BY c.customer_name")
            return cursor_customer.fetchall()

    def get_customer_by_id(self, customer_id):
        with self.db.cursor(dictionary=True) as cursor_customer:
            sql = "SELECT * FROM customer c WHERE c.id = %s"
            val = (customer_id, )
            cursor_customer.execute(sql, val)
            return cursor_customer.fetchone()
