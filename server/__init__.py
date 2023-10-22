from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import jsonify

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from server import models
from server.Auth.routes import auth_bp
from server.Positions.routes import positions_bp
from server.parsing.routes import parsing_bp
from server.calendar.calendar import calendar_bp
from server.statistics.routes import statistic_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(positions_bp, url_prefix='/positions')
app.register_blueprint(parsing_bp, url_prefix='/parsing')
app.register_blueprint(calendar_bp, url_prefix='/calendar')
app.register_blueprint(statistic_bp, url_prefix='/statistic')


@app.route('/')
def greetings():
    return jsonify(isError=False,
                   data={'message': 'Hi everyone on JobNinja API! Please, don`t break it. If you`ve found a bug '
                                    'text me to dimarvarek@gmail.com. For more information about this API check '
                                    'https://www.postman.com/telecoms-cosmonaut-24752222/workspace/jobninjaapi '
                                    'it will be here soon!'},
                   statusCode=200), 200


