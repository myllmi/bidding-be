from markitdown import MarkItDown

from db.resume_dao import ResumeDao
from service.queue_service import QueueService


class ResumeService:
    def __init__(self):
        pass
        self.db = ResumeDao()
        self.queue_service = QueueService()

    def insert_resume(self, resume_file):
        md = MarkItDown()  # Set to True to enable plugins
        result_md = md.convert(resume_file)
        resume_id = self.db.insert_resume(resume_file, result_md.text_content)
        self.queue_service.publish_event("resume.load", {"resume_id": resume_id})
        self.queue_service.close_connection()
