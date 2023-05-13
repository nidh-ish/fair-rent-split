from flaskapp.models import User
from flaskapp import bcrypt


def test_new_user(app):
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert bcrypt.check_password_hash(user.password, 'testing')
    assert user.history == ''

