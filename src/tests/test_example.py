import pytest
from voluntariat.models import User

# exemplu de fixtura


@pytest.fixture
def user(request, db):
    analiza_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    analiza_user.set_password('password_test')
    analiza_user.save()
    return analiza_user


# exemplu de test
def test_logout(client, user):
    client.force_login(user)
    resp = client.get('/logout/')
    assert resp.status_code == 302

# P.S: stiu ca testu astea pica acu da o sa treaca cand e implementat logou
