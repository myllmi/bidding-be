import uuid
from datetime import datetime, timezone

from db.dao import Dao


class ResumeDao(Dao):
    def insert_resume(self, file_path):
        resume_id = str(uuid.uuid4())
        with self.db.cursor(dictionary=True) as cursor_insert_resume:
            sql = "INSERT INTO bidding.resume (id, file_path_resume, status, created_at) VALUES (%s, %s, %s, %s)"
            val = (resume_id, str(file_path), '01', datetime.now(timezone.utc))
            cursor_insert_resume.execute(sql, val)
            self.db.commit()
        return resume_id
