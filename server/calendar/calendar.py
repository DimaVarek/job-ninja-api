import datetime
from server import db
from flask_login import current_user
from flask import request, jsonify, Blueprint
from server import models
from server.utils.utils import login_required_fop, change_stage_date_to_timestamp
from flask_cors import CORS, cross_origin


calendar_bp = Blueprint('calendar', 'calendar')
CORS(calendar_bp, supports_credentials=True)


@calendar_bp.route('/get_stages_by_period', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required_fop
def get_stages_by_period():
    try:
        owner_id = current_user.id
        start_interval = datetime.datetime.fromtimestamp(int(request.args['start_interval']))
        end_interval = datetime.datetime.fromtimestamp(int(request.args['end_interval']))
        stages = db.session.query(models.Stage).join(models.Position).filter(models.Position.owner_id == owner_id,
                                                                             models.Stage.date > start_interval,
                                                                             models.Stage.date < end_interval).all()
        stages = [change_stage_date_to_timestamp(i.to_dict()) for i in stages]
        return jsonify(isError=False,
                       data={"stages": stages},
                       message="Success",
                       statusCode=200), 200
    except:
        return jsonify(isError=True,
                       message="Some problems with this request",
                       statusCode=200), 200



