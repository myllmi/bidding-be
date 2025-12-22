import os
import uuid

from db.mysql_dao import MysqlDao
from dotenv import load_dotenv
from flask import Blueprint, request
from service.service_async import ServiceAsync
from werkzeug.utils import secure_filename

from util.helper import ResponseHelper

load_dotenv()
bidding_bp = Blueprint('bidding', __name__)


@bidding_bp.route('/', methods=['POST'])
def add_bidding():
    response_helper = ResponseHelper()
    #
    return response_helper.get_response()


@bidding_bp.route('/id/<id_bidding>', methods=['GET'])
def show_bidding(id_bidding):
    response_helper = ResponseHelper()
    dao = MysqlDao()
    dict_bidding = dao.get_bidding(id_bidding)
    response_helper.set_data({
        "id": id_bidding,
        "contract_authority": dict_bidding["contract_authority"],
        "reference": dict_bidding["reference"],
        "procedure_program_file": dict_bidding["procedure_program_file"],
        "notebook_charge_file": dict_bidding["notebook_charge_file"],
        "rational": dict_bidding["rational"],
    })
    return response_helper.get_response()


@bidding_bp.route('/list', methods=['GET'])
def get_all_bidding():
    response_helper = ResponseHelper()
    dao = MysqlDao()
    list_bidding = dao.get_all_bidding()
    arr_bidding = []
    for bidding in list_bidding:
        arr_bidding.append({
            "id": str(bidding["id"]),
            "contract_authority": bidding["contract_authority"],
            "reference": bidding["reference"],
            "procedure_program_file": bidding["procedure_program_file"],
            "notebook_charge_file": bidding["notebook_charge_file"],
            "created_at": bidding["created_at"].strftime("%d/%m/%Y") if bidding["created_at"] else None,
            "evaluated": bidding["evaluated"],
            "evaluated_at": bidding["evaluated_at"].strftime("%d/%m/%Y") if bidding["evaluated_at"] else None,
        })
    response_helper.set_data(arr_bidding)
    return response_helper.get_response()


@bidding_bp.route("/upload", methods=["POST"])
def upload_bidding():
    response_helper = ResponseHelper()

    if 'file' not in request.files:
        response_helper.set_code_message(_msg='No file part in the request')
        return response_helper.get_response()

    arr_file = []
    for file in request.files.getlist("file"):
        if file.filename == '':
            response_helper.set_code_message(_msg='No selected file')
            return response_helper.get_response()
        sec_filename = secure_filename(file.filename)
        arr_file.append(sec_filename)
        file.save(os.path.join(os.environ['UPLOAD_FOLDER_BIDDING'], sec_filename))

    dao = MysqlDao()
    service_async = ServiceAsync()
    id_async = uuid.uuid4()
    dao.add_temp_bidding(str(id_async), arr_file[0], arr_file[1])
    service_async.produce_bidding_extract(str(id_async))

    return response_helper.get_response()


@bidding_bp.route("/rational/<id_bidding>", methods=["POST"])
def rational_bidding(id_bidding):
    response_helper = ResponseHelper()
    service_async = ServiceAsync()
    service_async.produce_bidding_rational(id_bidding)
    dao = MysqlDao()
    dao.update_status_bid(id_bidding)
    return response_helper.get_response()
