import os
import uuid

from db.mysql_dao import MysqlDao
from dotenv import load_dotenv
from flask import Blueprint, request
from service.service_async import ServiceAsync
from werkzeug.utils import secure_filename

from util.helper import ResponseHelper

load_dotenv()
resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/', methods=['POST'])
def add_resume():
    response_helper = ResponseHelper()
    #
    return response_helper.get_response()


@resume_bp.route('/list', methods=['GET'])
def get_all_resume():
    response_helper = ResponseHelper()
    dao = MysqlDao()
    list_resume = dao.get_all_resume()
    arr_resume = []
    for resume in list_resume:
        arr_resume.append({
            "id": str(resume["id"]),
            "candidate_name": resume["candidate_name"],
            "profile": resume["profile"],
        })
    response_helper.set_data(arr_resume)
    return response_helper.get_response()


@resume_bp.route("/upload", methods=["POST"])
def upload_resume():
    response_helper = ResponseHelper()

    if 'file' not in request.files:
        response_helper.set_code_message(_msg='No file part in the request')
        return response_helper.get_response()

    dao = MysqlDao()
    service_async = ServiceAsync()
    for file in request.files.getlist("file"):
        if file.filename == '':
            response_helper.set_code_message(_msg='No selected file')
            return response_helper.get_response()
        sec_filename = secure_filename(file.filename)
        file.save(os.path.join(os.environ['UPLOAD_FOLDER_RESUME'], sec_filename))
        id_async = uuid.uuid4()
        dao.add_resume(str(id_async), sec_filename)
        service_async.produce_simple_extract(str(id_async))

    return response_helper.get_response()
