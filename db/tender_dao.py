import uuid
from datetime import datetime, timezone

from db.dao import Dao


class TenderDao(Dao):
    def insert_tender(self):
        tender_id = str(uuid.uuid4())
        with self.db.cursor(dictionary=True) as cursor_insert_resume:
            sql = "INSERT INTO bidding.tender (id, on_evaluation, customer_id, business_sector_id, analyst_id, manager_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (tender_id, 'N', '4bea566d-cd83-4fbd-a11a-95c55201598e', '5e48dd22-69bd-4db1-9e33-8f02104d20ad',
                   '59703a4d-e067-4fdc-8f87-82600d7764f2', '00351a51-ac4c-4c83-9e15-edf0beb64e38',
                   datetime.now(timezone.utc))
            cursor_insert_resume.execute(sql, val)
            self.db.commit()
        return tender_id

    def insert_tender_file(self, tender_id, file_name):
        with self.db.cursor(dictionary=True) as cursor_insert_tender_file:
            sql = "INSERT INTO bidding.tender_document (id, file_path_document, tender_id) VALUES (%s, %s, %s)"
            val = (str(uuid.uuid4()), file_name, tender_id)
            cursor_insert_tender_file.execute(sql, val)
            self.db.commit()

    def get_all_tender(self):
        with self.db.cursor(dictionary=True) as cursor_get_tender:
            sql = "SELECT t.*, c.customer_name FROM bidding.tender t LEFT JOIN bidding.customer c ON t.customer_id = c.id WHERE t.expired_at is null ORDER BY t.created_at DESC"
            cursor_get_tender.execute(sql)
            return cursor_get_tender.fetchall()
