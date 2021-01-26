# flash is the module and the Flask is the class

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

globalapp = Flask(__name__)
globalapp.config.from_object(Config)

db = SQLAlchemy(globalapp)
login = LoginManager(globalapp)
login.login_view = 'login'
migrate = Migrate(globalapp, db)

from app import routes, models
