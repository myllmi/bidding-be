from datetime import datetime

from db.dao import Dao

format_dt = '%Y-%m-%d %H:%M:%S'


class MysqlDao(Dao):
    def add_resume(self, _id, filename):
        with self.db.cursor() as cursor:
            sql = "INSERT INTO resume (id, filename, extracted, created_at) VALUES (%s, %s, %s, %s)"
            val = (_id, filename, 'N', datetime.now().strftime(format_dt))
            cursor.execute(sql, val)
            self.db.commit()

    def get_all_resume(self):
        with self.db.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM resume ORDER BY candidate_name"
            cursor.execute(sql)
            return cursor.fetchall()

    def add_temp_bidding(self, _id, file_1, file_2):
        with self.db.cursor() as cursor:
            sql = "INSERT INTO temp_bidding_file (id, file_1, file_2) VALUES (%s, %s, %s)"
            val = (_id, file_1, file_2)
            cursor.execute(sql, val)
            self.db.commit()

    def get_all_bidding(self):
        with self.db.cursor(dictionary=True) as cursor:
            sql = ("SELECT b.*, ca.name AS contract_authority "
                   "FROM bidding b LEFT JOIN contracting_authority ca "
                   "ON b.contracting_authority_id = ca.id ORDER BY created_at, reference")
            cursor.execute(sql)
            return cursor.fetchall()

    def get_all_project(self):
        with self.db.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM project ORDER BY customer_name, title"
            cursor.execute(sql)
            return cursor.fetchall()

    def get_bidding(self, id_bidding):
        with self.db.cursor(dictionary=True) as cursor:
            sql = ("SELECT b.*, ca.name AS contract_authority "
                   "FROM bidding b LEFT JOIN contracting_authority ca "
                   "ON b.contracting_authority_id = ca.id WHERE b.id = (%s)")
            cursor.execute(sql, (id_bidding,))
            return cursor.fetchone()

    def get_all_profile(self, id_bidding):
        with self.db.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM profile WHERE bidding_id = (%s)"
            cursor.execute(sql, (id_bidding,))
            return cursor.fetchall()

    def get_all_candidate(self, id_profile):
        with self.db.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM candidate WHERE profile_id = (%s)"
            cursor.execute(sql, (id_profile,))
            return cursor.fetchall()

    def update_status_bid(self, id_bid):
        with self.db.cursor() as cursor:
            sql = "UPDATE bidding SET evaluated = 1 WHERE id = (%s)"
            cursor.execute(sql, (id_bid,))
            self.db.commit()
