from server import db
from flask_login import current_user
from flask import jsonify, Blueprint
from flask_cors import CORS, cross_origin
from server import models
from server.utils.utils import login_required_fop
from server.statistics.utils import get_last_six_months, get_last_four_week, get_last_week
from sqlalchemy import func
from server.Enums.Enums import InterviewTypeEnum, InterviewStatusEnum


statistic_bp = Blueprint('statistics', 'statistics')
CORS(statistic_bp, supports_credentials=True)


@statistic_bp.route('/last_six_months', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required_fop
def last_six_months():
    owner_id = current_user.id
    six_months_dates = get_last_six_months()
    result = []
    number = 0
    for month in six_months_dates:
        applications = db.session.query(models.Position)\
            .filter(models.Position.owner_id == owner_id,
                    models.Position.created_on >= month[1],
                    models.Position.created_on <= month[2],
                    ).all()
        number += 1
        result.append({
            'id': number,
            'month': month[0],
            'applications': len(applications)
        })

    return jsonify(isError=False,
                   data=result,
                   message="Success",
                   statusCode=200), 200


@statistic_bp.route('/last_four_weeks', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required_fop
def last_four_weeks():
    owner_id = current_user.id
    four_weeks_dates = get_last_four_week()
    result = []
    for week in four_weeks_dates:
        applications = db.session.query(models.Position)\
            .filter(models.Position.owner_id == owner_id,
                    models.Position.created_on >= week[1],
                    models.Position.created_on <= week[2]).all()
        result.append({
            'week': week[0],
            'applications': len(applications)
        })

    return jsonify(isError=False,
                   data=result,
                   message="Success",
                   statusCode=200), 200


@statistic_bp.route('/last_week', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required_fop
def last_week():
    owner_id = current_user.id
    last_week_dates = get_last_week()
    result = []
    for day in last_week_dates:
        applications = db.session.query(models.Position)\
            .filter(models.Position.owner_id == owner_id,
                    models.Position.created_on >= day[1],
                    models.Position.created_on <= day[2]).all()
        result.append({
            'day': day[0],
            'applications': len(applications)
        })

    return jsonify(isError=False,
                   data=result,
                   message="Success",
                   statusCode=200), 200


@statistic_bp.route('/total_positive_result_by_each_stage', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required_fop
def total_positive_result_by_each_stage():
    owner_id = current_user.id
    result = db.session.query(models.Stage.type, func.count(models.Stage.type))\
        .join(models.Position)\
        .group_by(models.Stage.type)\
        .filter(models.Position.owner_id == owner_id,
                models.Stage.status == InterviewStatusEnum.Accepted).all()
    result = list(map(lambda x: {'stage': x[0].name, 'applications': x[1]}, result))
    all_types = [member.name for member in InterviewTypeEnum]
    for i in result:
        all_types.remove(i['stage'])
    for i in all_types:
        result.append({'stage': i, 'applications': 0})

    return jsonify(isError=False,
                   data=result,
                   message="Success",
                   statusCode=200), 200