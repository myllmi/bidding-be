from markitdown import MarkItDown

from db.tender_dao import TenderDao
from service.queue_service import QueueService


class TenderService:
    def __init__(self):
        self.db = TenderDao()
        self.queue_service = QueueService()

    def insert_tender(self, resume_file):
        # md = MarkItDown()  # Set to True to enable plugins
        # result_md = md.convert(resume_file)
        tender_id = self.db.insert_tender()
        self.queue_service.publish_event("tender.load", {"tender_id": tender_id})
        self.queue_service.close_connection()
