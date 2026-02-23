from db.tender_dao import TenderDao
from exception.business_exception import BusinessException
from service.queue_service import QueueService


class TenderService:
    def __init__(self):
        self.db = TenderDao()
        self.queue_service = QueueService()

    def insert_tender(self, arr_file):
        tender_id = self.db.insert_tender()  # TODO: Fix all fields in DAO
        for file in arr_file:
            self.db.insert_tender_file(tender_id, file)
        self.queue_service.publish_event("tender.load", {"tender_id": tender_id})
        self.queue_service.close_connection()

    def evaluate_tender(self, tender_id):
        self.queue_service.publish_event("tender.evaluate", {"tender_id": tender_id})

    def get_all_tender(self):
        return self.db.get_all_tender()

    def get_tender_by_id(self, tender_id):
        dict_tender = self.db.get_tender_by_id(tender_id)
        if dict_tender is None:
            raise BusinessException("Tender not found", 404)
        return dict_tender

    def get_tender_candidate(self, evaluation_id):
        dict_tender_candidate = self.db.get_tender_candidate(evaluation_id)
        if dict_tender_candidate is None:
            raise BusinessException("Candidates not found", 404)
        return dict_tender_candidate
