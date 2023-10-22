from server import db
from server.models import User
from flask_login import current_user, login_user, logout_user
from flask import request, jsonify, Blueprint


auth_bp = Blueprint('auth', 'auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify(isError=True,
                       message="You're already authenticated",
                       statusCode=200), 200
    try:
        data = request.json
        user = User.query.filter_by(username=data["username"]).first()
        if user is None or not user.check_password(data["password"]):
            return jsonify(isError=True,
                           message="Invalid username or password",
                           statusCode=200), 200
        login_user(user, remember=data["remember"])
        return jsonify(isError=False,
                       message="Success",
                       statusCode=200), 200
    except:
        return jsonify(isError=True,
                       message="Invalid request",
                       statusCode=200), 200


@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200), 200


@auth_bp.route('/is_auth', methods=['GET'])
def is_auth():
    if current_user.is_authenticated:
        return jsonify(isError=False,
                       data={"isAuth": True},
                       message="Success",
                       statusCode=200), 200
    return jsonify(isError=False,
                   data={"isAuth": False},
                   message="Current user is not authenticated",
                   statusCode=200), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify(isError=True,
                       message="This user's already exist",
                       statusCode=200), 200
    try:
        data = request.json
        user = User(username=data["username"],
                    email=data["email"],
                    first_name=data["first_name"],
                    last_name=data["last_name"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify(isError=False,
                       message="Success",
                       statusCode=200), 200
    except:
        return jsonify(isError=True,
                       message="Invalid request",
                       statusCode=200), 200





