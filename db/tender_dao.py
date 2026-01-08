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

    def get_tender_by_id(self, tender_id):
        with self.db.cursor(dictionary=True) as cursor_get_tender:
            sql = ("SELECT t.id, t.object, t.reference, t.on_evaluation, te.rational_md, c.customer_name, bs.sector_name, ua.name AS analyst_name, um.name AS manager_name, te.id AS evaluation_id "
                   "    FROM bidding.tender t "
                   "        LEFT JOIN bidding.tender_evaluation te ON te.tender_id = t.id "
                   "        LEFT JOIN bidding.customer c ON t.customer_id = c.id "
                   "        LEFT JOIN bidding.business_sector bs ON t.business_sector_id = bs.id "
                   "        LEFT JOIN bidding.user ua ON t.analyst_id = ua.id "
                   "        LEFT JOIN bidding.user um ON t.manager_id = um.id "
                   "    WHERE t.id = %s "
                   "        AND t.expired_at is null "
                   "        AND te.expired_at IS NULL")
            val = (tender_id,)
            cursor_get_tender.execute(sql, val)
            return cursor_get_tender.fetchone()

    def get_tender_candidate(self, evaluation_id):
        with self.db.cursor(dictionary=True) as cursor_get_tender_candidate:
            sql = "SELECT tc.*, r.name_professional FROM bidding.tender_candidate tc LEFT JOIN bidding.resume r ON tc.resume_id = r.id WHERE tc.evaluation_id = %s"
            val = (evaluation_id,)
            cursor_get_tender_candidate.execute(sql, val)
            return cursor_get_tender_candidate.fetchall()
