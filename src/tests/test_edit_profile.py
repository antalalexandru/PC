import pytest

from voluntariat.forms import ChangePasswordForm
from voluntariat.models import User


@pytest.fixture
def user(db):
    logged_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    logged_user.set_password('password_test')
    logged_user.save()

    return logged_user


def test_myProfile(user, client):
    client.force_login(user)
    resp = client.get('/myprofile/')
    assert resp.status_code == 200
    assert client.get('/myprofile/update/').status_code == 200
    assert client.get('/myprofile/changePassword/').status_code == 200
    client.logout()



def test_validForm(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/changePassword/', data={'old_password': 'password_test',
                                                           'new_password': '1234',
                                                           'repeat_password': '1234'})
    assert resp.status_code == 302

    user = User.objects.get(id=user.id)
    assert user.check_password("1234")
    client.logout()
    user.delete()


def test_differentNewPassAndRepeatPass(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/changePassword/', data={'old_password': 'password_test',
                                                           'new_password': 'eqweqwe',
                                                           'repeat_password': '12qwewq35'})
    assert resp.status_code == 200
    user = User.objects.get(id=user.id)
    assert user.check_password("password_test")
    client.logout()
    user.delete()


def test_invalidOldPassword(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/changePassword/', data={'old_password': 'invalid',
                                                           'new_password': '1234',
                                                           'repeat_password': '1234'})
    assert resp.status_code == 200
    user = User.objects.get(id=user.id)
    assert user.check_password("password_test")
    client.logout()
    user.delete()


def test_sameNewPass(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/changePassword/', data={'old_password': 'password_test',
                                                           'new_password': 'password_test',
                                                           'repeat_password': 'password_test'})
    assert resp.status_code == 200
    user = User.objects.get(id=user.id)
    assert user.check_password("password_test")
    client.logout()
    user.delete()


def test_ModifyDescription(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/update/', data={'personal_description': '1234'})

    assert resp.status_code == 302
    user = User.objects.get(id=user.id)
    assert user.personal_description == '1234'
    client.logout()
    user.delete()

def test_ModifyEmptyDescription(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/update/', data={'personal_description': ''})

    assert resp.status_code == 200
    client.logout()
    user.delete()
