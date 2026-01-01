from db.tender_dao import TenderDao
from service.queue_service import QueueService


class TenderService:
    def __init__(self):
        self.db = TenderDao()
        self.queue_service = QueueService()

    def insert_tender(self, arr_file):
        tender_id = self.db.insert_tender() # TODO: Fix all fields in DAO
        for file in arr_file:
            self.db.insert_tender_file(tender_id, file)
        self.queue_service.publish_event("tender.load", {"tender_id": tender_id})
        self.queue_service.close_connection()
