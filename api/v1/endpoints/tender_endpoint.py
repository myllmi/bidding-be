import shutil
from pathlib import Path as FsPath
from typing import List

from anyio import sleep
from fastapi import APIRouter, Depends, UploadFile, File

from filter.request_filter import check_access_token
from service.tender_service import TenderService

router = APIRouter()


@router.post("/upload",
             summary="Upload Tender Files",
             description="Upload Tender Files",
             dependencies=[Depends(check_access_token)])
def upload_files_tender(files: List[UploadFile] = File(...), tender_service: TenderService = Depends(TenderService)):
    upload_dir = FsPath("/in/tender")
    arr_file = []
    for file in files:
        file_path = upload_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            arr_file.append(str(file_path))
    tender_service.insert_tender(arr_file)
    return {}


@router.post("/evaluate/{tender_id}",
             summary="Evaluate Tender",
             description="Evaluate Files",
             dependencies=[Depends(check_access_token)])
def evaluate_tender(tender_id: str, tender_service: TenderService = Depends(TenderService)):
    tender_service.evaluate_tender(tender_id)
    return {}

@router.get("/list",
             summary="List Tenders",
             description="List Tenders",
            dependencies=[Depends(check_access_token)])
def list_tenders():
    tender_service = TenderService()
    return tender_service.get_all_tender()

@router.get("/{tender_id}",
            summary="Get Tender",
            description="Get Tender",
            dependencies=[Depends(check_access_token)])
def get_tender(tender_id: str):
    tender_service = TenderService()
    return tender_service.get_tender_by_id(tender_id)

@router.get("/candidate/{evaluation_id}",
            summary="Get Tender Candidates",
            description="Get Tender Candidates",
            dependencies=[Depends(check_access_token)])
def get_tender_candidates(evaluation_id: str):
    tender_service = TenderService()
    return tender_service.get_tender_candidate(evaluation_id)