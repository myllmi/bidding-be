from db.mysql_dao import MysqlDao
from dotenv import load_dotenv
from flask import Blueprint, request
from service.service_async import ServiceAsync
from werkzeug.utils import secure_filename

from util.helper import ResponseHelper

load_dotenv()
profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/', methods=['POST'])
def add_profile():
    response_helper = ResponseHelper()
    #
    return response_helper.get_response()


@profile_bp.route('/list/<id_bidding>', methods=['GET'])
def get_all_profile(id_bidding):
    response_helper = ResponseHelper()
    dao = MysqlDao()
    list_profile = dao.get_all_profile(id_bidding)
    arr_profile = []
    for profile in list_profile:
        arr_profile.append({
            "id": str(profile["id"]),
            "name": profile["name"],
            "description": profile["description"],
        })
    response_helper.set_data(arr_profile)
    return response_helper.get_response()
