import pytest

from voluntariat.models import User

#
# @pytest.fixture
# def user(db):
#     analiza_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
#     analiza_user.set_password('password_test')
#     analiza_user.save()
#     return analiza_user


def test_myprofile(client,db):
    user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    user.set_password('password_test')
    user.save()
    assert client.get('/myprofile/').status_code == 404
    assert client.get('/myprofile/' + str(user.id)).status_code == 301
    assert client.get('/myprofile/' + str(user.id) + '/update').status_code == 200
    assert client.get('/myprofile/' + str(user.id) + '/changePassword').status_code == 200

    assert client.post('/myprofile/' + str(user.id) + '/changePassword',
                       {'old_password': 'password_test', 'new_password': '1234',
                        'repeat_password': '1234', 'user': user}).status_code == 302

    assert user.check_password("1234")
    user.delete()

    # assert client.post('/login/', {'username': 'user_test_temporary', 'password': 'password_test'}).status_code == 400
    # assert client.post('/login/', {'username': 'user_test_temporary'}).status_code == 200
