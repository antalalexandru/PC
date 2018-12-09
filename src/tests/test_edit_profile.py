import pytest

from voluntariat.forms import ChangePasswordForm
from voluntariat.models import User


@pytest.fixture
def user(db):
    logged_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    logged_user.set_password('password_test')
    logged_user.save()
    return logged_user


def test_myprofile(user, client):
    client.force_login(user)

    resp = client.get('/myprofile/')
    assert resp.status_code == 200

    assert client.get('/myprofile/update/').status_code == 200
    assert client.get('/myprofile/changePassword/').status_code == 200

    resp = client.post('/myprofile/changePassword/', data={'old_password': 'password_test',
                                                           'new_password': '1234',
                                                           'repeat_password': '1234'})
    assert resp.status_code == 302

    user = User.objects.get(id=user.id)
    assert user.check_password("1234")
    user.delete()

    # assert client.post('/login/', {'username': 'user_test_temporary', 'password': 'passoword_test'}).status_code == 400
    # assert client.post('/login/', {'username': 'user_test_temporary'}).status_code == 200
