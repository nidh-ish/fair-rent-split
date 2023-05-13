import pytest
from flaskapp import create_app, db, bcrypt
from flaskapp.models import User
from sqlalchemy import delete

@pytest.fixture(scope='session')
def app():
    app = create_app(test_config={'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 'WTF_CSRF_ENABLED': False})
    app_context = app.app_context()
    app_context.push()

    with app.app_context():
        db.create_all()

        hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
        user = User(username='testuser', email='testuser@example.com', password=hashed_password, history='')
        db.session.add(user)
        db.session.commit()

    yield app

    app_context.pop()

@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def clean_db(app):
    with app.app_context():
        db.session.execute(delete(User))
        db.session.commit()

@pytest.fixture
def new_user():
    hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
    user = User(username='testuser', email='testuser@example.com', password=hashed_password, history='')
    return user
