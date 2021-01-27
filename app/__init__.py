# flash is the module and the Flask is the class


from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

globalapp = Flask(__name__)
globalapp.config.from_object(Config)

db = SQLAlchemy(globalapp)
login = LoginManager(globalapp)
login.login_view = 'login'
migrate = Migrate(globalapp, db)

if not globalapp.debug:
    if globalapp.config['MAIL_SERVER']:
        auth = None
        if globalapp.config['MAIL_USERNAME'] or globalapp.config['MAIL_PASSWORD']:
            auth = (globalapp.config['MAIL_USERNAME'], globalapp.config['MAIL_PASSWORD'])
        secure = None
        if globalapp.config['MAIL_USE_TLS']:
            globalapp = ()
        mail_handler = SMTPHandler(
            mailhost=(globalapp.config['MAIL_SERVER'], globalapp.config['MAIL_PORT']),
            fromaddr='no-reply@' + globalapp.config['MAIL_SERVER'],
            toaddrs=globalapp.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        globalapp.logger.addHandler(mail_handler)

if not globalapp.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    globalapp.logger.addHandler(file_handler)

    globalapp.logger.setLevel(logging.INFO)
    globalapp.logger.info('Microblog startup')

from app import routes, models, errors