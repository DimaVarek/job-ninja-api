from flask_login import current_user
from flask import jsonify
from server.models import Position
from datetime import datetime


# login required for our project
def login_required_fop(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        return jsonify(isError=True,
                       message="current user is not authenticated",
                       statusCode=200), 200
    wrapper.__name__ = func.__name__
    return wrapper


# change position after serializing
def change_position_date_to_timestamp(position):
    position['created_on'] = datetime.strptime(position['created_on'], '%Y-%m-%d %H:%M:%S').timestamp()
    position['updated_on'] = datetime.strptime(position['updated_on'], '%Y-%m-%d %H:%M:%S').timestamp()
    for i in range(len(position['stages'])):
        position['stages'][i] = change_stage_date_to_timestamp(position['stages'][i])
    return position


# change stage after serializing
def change_stage_date_to_timestamp(stage):
    stage['date'] = datetime.strptime(stage['date'], '%Y-%m-%d %H:%M:%S').timestamp()
    return stage

