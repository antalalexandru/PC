import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

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
    resp = client.post('/myprofile/update/', data={'picture': '', 'personal_description': ''})

    assert resp.status_code == 302
    client.logout()
    user.delete()


def test_ModifyProfileImage(user, client):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    client.force_login(user)
    resp = client.post('/myprofile/update/', data={'picture': uploaded, 'personal_description': ''})
    user = User.objects.get(id=user.id)
    assert resp.status_code == 302
    client.logout()
    user.delete()


def test_failModifyProfileImage(user, client):
    client.force_login(user)
    resp = client.post('/myprofile/update/', data={'picture': '', 'personal_description': 'sugi'})
    assert resp.status_code == 200
    client.logout()
    user.delete()
