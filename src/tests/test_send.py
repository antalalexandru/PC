import pytest
from django.db.models import QuerySet
from voluntariat.models import Event, User, Participantion
from django.urls import reverse
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock


@pytest.fixture
def user_instance(request, db):
    analiza_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    analiza_user.set_password('password_test')
    analiza_user.save()
    return analiza_user


@pytest.fixture
def event_instance(user_instance):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    date = datetime.now()

    return Event.objects.create(name='Denis', picture=uploaded, location='Cluj', description='Cluj', \
                                benefits='Cluj', start_date=date, end_date=date, organizer=user_instance)


def fake_send(self, fail_silently=False):
    """Send the email message."""
    pass


'''
def test_signup(client, user):
    assert client.get('/signup/').status_code == 200
    form_data = {'username': 'invalid_username', 'first_name': 'a', 'last_name': 'b', 'email': 'email@user.ro', 'password1': '1234', 'password2': '1234'}
    resp = client.post('/signup/', form_data)
    assert resp.status_code == 200
    assert client.post('/signup/', {'username': 'invalid_username2', 'first_name': 'a1', 'last_name': 'b2', 'email': 'email2@user.ro', 'password1': '@!NVIDIA9857481', 'password2': '@!NVIDIA9857481'}).status_code == 302


'''


def test_send_email(client, user_instance, event_instance, db):
    client.force_login(user_instance)
    lungime = len(Participantion.objects.all())
    assert lungime == 0
    client.post(reverse('voluntariat:event-attend', kwargs={'pk': event_instance.pk}))
    assert len(Participantion.objects.all()) == 1
    client.logout()
    form_data = {'message': 'valid msg'}
    resp = client.post('/sendinfo/', form_data)

    assert (list(
        Event.objects.get(pk=event_instance.pk).participantion_set.filter().prefetch_related("voluntar").values_list(
            "voluntar__email", flat=True)) == ['user_test@test.com'])
    with mock.patch('django.core.mail.message.EmailMessage.send', fake_send):
        resp = client.post(reverse('voluntariat:sendinfo', kwargs={'pk': event_instance.pk}))

        assert resp.status_code == 302
