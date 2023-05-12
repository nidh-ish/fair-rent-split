from flaskapp  import db, login_manager
from flask import current_app  
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from datetime import datetime, timedelta
 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False )
    password = db.Column(db.String(60), nullable=False)
    history = db.Column(db.String(8000), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        expiration = datetime.utcnow() + timedelta(seconds=expires_sec)
        payload = {'user_id': self.id, 'expires': expiration.timestamp()}
        return s.dumps(payload, salt='reset-token-salt')

    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            payload = s.loads(token, salt='reset-token-salt')
            user_id = payload['user_id']
            expires = datetime.fromtimestamp(payload['expires'])
            if expires < datetime.utcnow():
                return None
            user = User.query.get(user_id)
            return user
        except:
            return None
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}'" 