from db.mysql_dao import MysqlDao
from dotenv import load_dotenv
from flask import Blueprint, request
from service.service_async import ServiceAsync
from werkzeug.utils import secure_filename

from util.helper import ResponseHelper

load_dotenv()
project_bp = Blueprint('project', __name__)


@project_bp.route('/', methods=['POST'])
def add_project():
    response_helper = ResponseHelper()
    #
    return response_helper.get_response()


@project_bp.route('/list', methods=['GET'])
def get_all_project():
    response_helper = ResponseHelper()
    dao = MysqlDao()
    list_project = dao.get_all_project()
    arr_project = []
    for project in list_project:
        arr_project.append({
            "id": str(project["id"]),
            "customer_name": project["customer_name"],
            "title": project["title"],
            "business_sector": project["business_sector"],
        })
    response_helper.set_data(arr_project)
    return response_helper.get_response()
