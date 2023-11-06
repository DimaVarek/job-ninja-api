import datetime

from server import db
from flask_login import current_user
from flask import request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from server import models
from server.utils.utils import login_required_fop, change_position_date_to_timestamp


positions_bp = Blueprint('positions', 'positions')
CORS(positions_bp, supports_credentials=True)


@positions_bp.route("/positions", methods=["GET"])
@cross_origin(supports_credentials=True)
@login_required_fop
def get_positions():
    owner_id = current_user.id
    positions = models.Position.query.filter_by(owner_id=owner_id).all()
    if positions is None:
        positions = []
    positions = [change_position_date_to_timestamp(i.to_dict()) for i in positions]
    return jsonify(isError=False,
                   data=positions,
                   message="Success",
                   statusCode=200), 200


@positions_bp.route("/add_position", methods=["POST"])
@cross_origin(supports_credentials=True)
@login_required_fop
def add_position():
    owner_id = current_user.id
    data = request.json
    position = models.Position(owner_id=owner_id,
                               position_link=data.get('position_link'),
                               company_name=data.get("company_name"),
                               position_name=data.get("position_name"),
                               company_image_link=data.get("company_image_link"),
                               description=data.get("description"))
    stages = []
    if data.get("interview_stages"):
        for i in range(len(data["interview_stages"])):
            stage = models.Stage(position_id=position.id,
                                 number_in_order=i,
                                 interview_type=data["interview_stages"][i].get("interview_type"),
                                 interview_status=data["interview_stages"][i].get("interview_status"),
                                 comment=data["interview_stages"][i].get("comment"),
                                 date=datetime.datetime.fromtimestamp(int(data["interview_stages"][i].get("date"))))
            stages.append(stage)
        position.interview_stages = stages
    try:
        db.session.add(position)
        db.session.commit()
        return jsonify(isError=False,
                       data={"id": position.id},
                       message="Success",
                       statusCode=200), 200
    except:
        db.session.rollback()
        return jsonify(isError=True,
                       message="Something went wrong",
                       statusCode=200), 200


@positions_bp.route('/position/<position_id>', methods=["GET", "PUT", "DELETE"])
@cross_origin(supports_credentials=True)
@login_required_fop
def position(position_id):
    owner_id = current_user.id
    pos: models.Position = models.Position.query.filter_by(owner_id=owner_id, id=position_id).first()
    if pos is None:
        return jsonify(isError=True,
                       message="We dont have this position",
                       statusCode=200), 200
    if request.method == "GET":
        return jsonify(isError=False,
                       data=change_position_date_to_timestamp(pos.to_dict()),
                       message="Success",
                       statusCode=200), 200
    elif request.method == "PUT":
        try:
            data = request.json
            pos.position_link = data.get('position_link')
            pos.company_name = data.get('company_name')
            pos.position_name = data.get("position_name")
            pos.company_image_link = data.get('company_image_link')
            pos.description = data.get('description')
            for i in pos.interview_stages:
                db.session.delete(i)
            stages = []
            if data.get("interview_stages"):
                for i in range(len(data["interview_stages"])):
                    stage = models.Stage(position_id=pos.id,
                                         number_in_order=i,
                                         interview_type=data["interview_stages"][i].get("interview_type"),
                                         interview_status=data["interview_stages"][i].get("interview_status"),
                                         comment=data["interview_stages"][i].get("comment"),
                                         date=datetime.datetime.fromtimestamp(int(data["interview_stages"][i].get("date"))))
                    stages.append(stage)
                pos.interview_stages = stages
            db.session.commit()
            return jsonify(isError=False,
                           message="Success update",
                           statusCode=200), 200
        except:
            db.session.rollback()
            return jsonify(isError=True,
                           message="Some problems with update",
                           statusCode=200), 200

    elif request.method == "DELETE":
        try:
            for i in pos.interview_stages:
                db.session.delete(i)
            db.session.delete(pos)
            db.session.commit()
            return jsonify(isError=False,
                           message="Success delete",
                           statusCode=200), 200
        except:
            db.session.rollback()
            return jsonify(isError=True,
                           message="Some problems with delete",
                           statusCode=200), 200





