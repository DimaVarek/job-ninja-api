from flask_login import UserMixin
from datetime import datetime
from .Enums.Enums import InterviewStatusEnum, InterviewTypeEnum
from server import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Position(db.Model, SerializerMixin):
    __tablename__ = "positions"

    serialize_only = ('id', 'position_link', 'company_name', 'position_name', 'company_image_link', 'description',
                      'created_on', 'updated_on', 'stages')

    serialize_rules = ('-stages.position',)

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    position_link = db.Column(db.String(256), default='linkedin.com')
    company_name = db.Column(db.String(256), default='')
    position_name = db.Column(db.String(256), default='')
    company_image_link = db.Column(db.String(256), default='linkedin.com')
    description = db.Column(db.Text(), default='')
    created_on = db.Column(db.TIMESTAMP(), default=datetime.utcnow)
    updated_on = db.Column(db.TIMESTAMP(), default=datetime.utcnow, onupdate=datetime.utcnow)
    stages = db.relationship('Stage', backref='position')


class Stage(db.Model, SerializerMixin):
    __tablename__ = "stages"

    serialize_only = ('id', 'position_id', 'number_in_order', 'interview_type',
                      'interview_status', 'comment', 'date')
    serialize_rules = ('-position',)

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    position_id = db.Column(db.Integer(), db.ForeignKey('positions.id'), nullable=False)
    number_in_order = db.Column(db.Integer(), nullable=False)
    interview_type = db.Column(db.Enum(InterviewTypeEnum))
    interview_status = db.Column(db.Enum(InterviewStatusEnum))
    comment = db.Column(db.Text(), default='')
    date = db.Column(db.TIMESTAMP(), default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    positions = db.relationship('Position', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)











