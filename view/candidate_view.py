from db.mysql_dao import MysqlDao
from dotenv import load_dotenv
from flask import Blueprint, request
from service.service_async import ServiceAsync
from werkzeug.utils import secure_filename

from util.helper import ResponseHelper

load_dotenv()
candidate_bp = Blueprint('candidate', __name__)


@candidate_bp.route('/', methods=['POST'])
def add_profile():
    response_helper = ResponseHelper()
    #
    return response_helper.get_response()


@candidate_bp.route('/list/<id_profile>', methods=['GET'])
def get_all_profile(id_profile):
    response_helper = ResponseHelper()
    dao = MysqlDao()
    list_candidate = dao.get_all_candidate(id_profile)
    arr_candidate = []
    for candidate in list_candidate:
        arr_candidate.append({
            "id": str(candidate["id"]),
            "name": candidate["name"],
            "final_resume": candidate["final_resume"],
        })
    response_helper.set_data(arr_candidate)
    return response_helper.get_response()
