import pytest
from voluntariat.models import User

# exemplu de fixtura


@pytest.fixture
def user(request, db):
    analiza_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    analiza_user.set_password('password_test')
    analiza_user.save()
    return analiza_user

def test_login(client, user):
    assert client.get('/login/').status_code == 200
    assert client.post('/login/', {'username': 'invalid_username', 'password': '1234'}).status_code == 400
    assert client.post('/login/', {'username': 'user_test', 'password': 'password_test'}).status_code == 302

def test_signup(client, user):
    assert client.get('/signup/').status_code == 200
    assert client.post('/signup/', {'username': 'invalid_username', 'first_name': 'a', 'last_name': 'b', 'email': 'email@user.ro', 'password1': '1234', 'password2': '1234'}).status_code == 400

# exemplu de test
def test_logout(client, user):
    client.force_login(user)
    resp = client.get('/logout/')
    assert resp.status_code == 302

# P.S: stiu ca testu astea pica acu da o sa treaca cand e implementat logou
