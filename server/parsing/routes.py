from server import db
from flask import Blueprint, request, jsonify
from server.parsing.utils import get_vacancy

parsing_bp = Blueprint('parsing', 'parsing')


@parsing_bp.route('/', methods=["POST"])
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