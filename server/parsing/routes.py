from server import db
from flask import Blueprint, request, jsonify
from server.parsing.utils import get_vacancy
from server.utils.utils import login_required_fop
from flask_cors import CORS, cross_origin

parsing_bp = Blueprint('parsing', 'parsing')
CORS(parsing_bp, supports_credentials=True)


@parsing_bp.route('/', methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required_fop
def parsing():
    try:
        data_url = request.json
        result = get_vacancy(data_url['url'])
        return jsonify(isError=False,
                       data=result,
                       message="Success",
                       statusCode=200), 200
    except:
        return jsonify(isError=True,
                       message="Some error with parsing",
                       statusCode=200), 200