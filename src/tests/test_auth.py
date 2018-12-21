import pytest
from voluntariat.models import User


@pytest.fixture
def user(request, db):
    analiza_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    analiza_user.set_password('password_test')
    analiza_user.save()
    return analiza_user


def test_login(client, user):
    assert client.get('/login/').status_code == 200
    user = User.objects.create(username='user_test_temporary', email='user_test@test.com', age=18)
    user.set_password('password_test')
    user.save()
    assert client.post('/login/', {'username': 'user_test_temporary', 'password': 'password_test'}).status_code == 302
    user.delete()
    assert client.post('/login/', {'username': 'user_test_temporary', 'password': 'password_test'}).status_code == 400
    assert client.post('/login/', {'username': 'user_test_temporary'}).status_code == 200


def test_signup(client, user):
    assert client.get('/signup/').status_code == 200
    form_data = {'username': 'invalid_username', 'first_name': 'a', 'last_name': 'b', 'email': 'email@user.ro', 'password1': '1234', 'password2': '1234'}
    resp = client.post('/signup/', form_data)
    assert resp.status_code == 200
    assert client.post('/signup/', {'username': 'invalid_username2', 'first_name': 'a1', 'last_name': 'b2', 'email': 'email2@user.ro', 'password1': '@!NVIDIA9857481', 'password2': '@!NVIDIA9857481'}).status_code == 302


def test_logout(client, user):
    client.force_login(user)
    resp = client.get('/logout/')
    assert resp.status_code == 302

