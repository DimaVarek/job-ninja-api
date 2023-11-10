from server import db, mail, app
from server.models import User
from flask_login import current_user, login_user, logout_user
from flask import request, jsonify, Blueprint
from flask_mail import Message
from server.utils.utils import login_required_fop
from flask_cors import CORS, cross_origin


auth_bp = Blueprint('auth', 'auth')

CORS(auth_bp, supports_credentials=True)


@auth_bp.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def logout():
    logout_user()
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200), 200


@auth_bp.route('/is_auth', methods=['GET'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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


@auth_bp.route('/request_reset_password', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def request_reset_password():
    current_id = -1
    if request.method == 'GET' and current_user.is_authenticated:
        current_id = current_user.id
    if request.method == 'POST':
        data = request.json
        current_email = data['email']
        current_user_local = User.query.filter(User.email == current_email).first()
        if current_user_local:
            current_id = current_user_local.id

    if current_id != -1:
        user = User.query.filter(User.id == current_id).first()
        token = user.get_reset_password_token()
        msg = Message(
            'Request',
            sender=app.config['MAIL_USERNAME'],
            recipients=user.email.split()
        )
        msg.body = f'http://localhost:3000/reset_password/{token}'
        mail.send(msg)
        return jsonify(isError=False,
                       message="Success",
                       statusCode=200), 200
    return jsonify(isError=True,
                   message="User doesn't exist or you use wrong method",
                   statusCode=200), 200


@auth_bp.route('/reset_password', methods=['POST'])
@cross_origin(supports_credentials=True)
def reset_password():
    data = request.json
    token = data['token']
    new_password = data['new_password']
    user: User = User.verify_reset_password_token(token)
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify(isError=False,
                       message="Password was changed successful",
                       statusCode=200), 200
    return jsonify(isError=True,
                   message="Token has expired or wrong params of request",
                   statusCode=200), 200


@auth_bp.route('/user_info', methods=['GET'])
@cross_origin(supports_credentials=True)
@login_required_fop
def get_user_info():
    our_user: User = User.query.filter(User.id == current_user.id).first()
    return jsonify(isError=False,
                   data={'user': our_user.to_dict()},
                   message="Password was changed successful",
                   statusCode=200), 200


