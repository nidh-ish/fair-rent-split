from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_mail import Mail
from flaskapp.config import Config
import logging
import logging.config
from pythonjsonlogger import jsonlogger

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()  
login_manager = LoginManager()  
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #comment if we want previous log also
    #with open('instance/app.log', 'w'):
    #    pass
    
    handler = logging.handlers.RotatingFileHandler('instance/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    # formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
    formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    
    app.logger.setLevel(logging.INFO)

    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskapp.users.routes import users
    from flaskapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)
    
    return app
