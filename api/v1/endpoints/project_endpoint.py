import shutil
from pathlib import Path as FsPath

from fastapi import APIRouter, Depends, UploadFile, File

from filter.request_filter import check_access_token, check_admin_role
from service.project_service import ProjectService

router = APIRouter()

@router.post("/upload",
             summary="Upload List of Projects (XLS)",
             description="Upload List of Projects (XLS)",
             dependencies=[Depends(check_access_token), Depends(check_admin_role)],)
def upload_file_project(file: UploadFile = File(...), project_service: ProjectService = Depends(ProjectService)):
    upload_dir = FsPath("/in/project")
    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    project_service.insert_project(file_path)
    return {}

@router.get("/list",
            summary="List all projects",
            description="List all projects",
            dependencies=[Depends(check_access_token)])
def list_projects(project_service: ProjectService = Depends(ProjectService)):
    return project_service.get_all_projects()