from flaskapp.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm

def test_registration_form_valid(client, app):
    form = RegistrationForm()
    form.username.data = 'newuser'
    form.email.data = 'newuser@example.com'
    form.password.data = 'password'
    form.confirm_password.data = 'password'
    assert form.validate() is True

def test_registration_form_invalid_username(client, app):
    form = RegistrationForm()
    form.username.data = 'invalid_username!'
    form.email.data = 'newuser@example.com'
    form.password.data = 'password'
    form.confirm_password.data = 'password'
    assert form.validate() is False
    assert 'Invalid username. Only alphanumeric characters are allowed.' in form.username.errors

def test_registration_form_existing_username(client, app, new_user):
    form = RegistrationForm()
    form.username.data = new_user.username
    form.email.data = 'newuser@example.com'
    form.password.data = 'password'
    form.confirm_password.data = 'password'
    assert form.validate() is False
    assert 'That username is already taken. Try again with different username' in form.username.errors

def test_registration_form_existing_email(client, app, new_user):
    form = RegistrationForm()
    form.username.data = 'newuser'
    form.email.data = new_user.email
    form.password.data = 'password'
    form.confirm_password.data = 'password'
    assert form.validate() is False
    assert 'That email is already taken. Try again with different email' in form.email.errors


def test_login_form_valid(client, new_user):
    form = LoginForm()
    form.email.data = new_user.email
    form.password.data = new_user.password
    assert form.validate() is True

def test_login_form_invalid_email(client):
    form = LoginForm()
    form.email.data = 'invalid_email'
    form.password.data = 'password'
    assert form.validate() is False
    assert any('Invalid email address' in error for error in form.errors['email'])

def test_request_reset_form_valid(client, app, new_user):
    form = RequestResetForm()
    form.email.data = new_user.email
    assert form.validate() is True

def test_request_reset_form_invalid_email(client):
    form = RequestResetForm()
    form.email.data = 'invalid_email'
    assert form.validate() is False
    assert 'Invalid email address.', 'There is no account with that email.' in form.email.errors

def test_reset_password_form_valid(client):
    form = ResetPasswordForm()
    form.password.data = 'new_password'
    form.confirm_password.data = 'new_password'
    assert form.validate() is True

def test_reset_password_form_invalid_confirm_password(client):
    form = ResetPasswordForm()
    form.password.data = 'new_password'
    form.confirm_password.data = 'different_password'
    assert form.validate() is False
    assert 'Field must be equal to password.' in form.confirm_password.errors



