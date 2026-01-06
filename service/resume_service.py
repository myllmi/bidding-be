from db.resume_dao import ResumeDao
from service.queue_service import QueueService


class ResumeService:
    def __init__(self):
        self.db = ResumeDao()
        self.queue_service = QueueService()

    def insert_resume(self, arr_file):
        for resume_file in arr_file:
            resume_id = self.db.insert_resume(resume_file)
            self.queue_service.publish_event("resume.load", {"resume_id": resume_id})
        self.queue_service.close_connection()

    def list_resume(self):
        return self.db.list_resume()
