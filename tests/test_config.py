from flaskapp import create_app

def test_config(app):
    assert app.config['TESTING'] == True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
