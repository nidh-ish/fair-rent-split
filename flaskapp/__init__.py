from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_mail import Mail

app = Flask(__name__) 
app.config['SECRET_KEY'] = '6540cd44ed6d2d1b06d7b6451b404d6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mynotesappbyflask@gmail.com'
app.config['MAIL_PASSWORD'] = "ntvluojufenocqtw "
 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)  
login_manager = LoginManager(app)  
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskapp import routes