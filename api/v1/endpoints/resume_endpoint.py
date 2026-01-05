import shutil
from pathlib import Path as FsPath
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File

from filter.request_filter import check_access_token
from service.resume_service import ResumeService

router = APIRouter()


@router.post("/upload",
             summary="Upload Resume File",
             description="Upload Resume File",
             dependencies=[Depends(check_access_token)])
def upload_file_resume(files: List[UploadFile] = File(...), resume_service: ResumeService = Depends(ResumeService)):
    upload_dir = FsPath("/in/resume")
    arr_file = []
    for file in files:
        file_path = upload_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            arr_file.append(str(file_path))
    resume_service.insert_resume(arr_file)
    return {}
