import pytest
from voluntariat.models import Event, User, Participantion
from django.urls import reverse
from django.db import models
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def user_instance(request, db):
    analiza_user = User.objects.create(username='user_test', email='user_test@test.com', age=18)
    analiza_user.set_password('password_test')
    analiza_user.save()
    return analiza_user

@pytest.fixture
def user_instance2(request, db):
    analiza_user = User.objects.create(username='user_test2', email='user_test2@test.com', age=18)
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

    return Event.objects.create(name='Denis', picture=uploaded, location='Cluj', description='Cluj',\
                                benefits='Cluj', start_date=date, end_date=date, organizer=user_instance)

@pytest.fixture
def event(request, db):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    date = datetime.now()

    data = {'name': 'Denis', 'picture': uploaded, 'location': 'Cluj'
        , 'description': 'Cluj', 'benefits': 'Cluj', 'start_date': date, 'end_date': date}

    return data


@pytest.fixture
def event2(request, db):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    date = datetime.now()

    data = {'name': 'Bla', 'picture': uploaded, 'location': 'Cluj'
        , 'description': 'Cluj', 'benefits': 'Cluj', 'start_date': date, 'end_date': date}

    return data


@pytest.fixture
def event3(request, db):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    date = datetime.now()

    data = {'name': 'Roland', 'picture': uploaded, 'location': 'Cluj'
        , 'description': 'Cluj', 'benefits': 'Cluj', 'start_date': date, 'end_date': date}

    return data


def test_add(client, event, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    resp = client.post(reverse('voluntariat:create'), event)
    assert Event.objects.filter(name='Denis').exists()

    assert (resp.status_code == 302)
    resp1 = client.get(reverse('voluntariat:dashboard'))

    assert len(resp1.context['my_event_list']) == 1
    responseGet = client.get(reverse('voluntariat:create'), event)
    assert responseGet.status_code == 200


def test_add_fail(client, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)

    eventx = {'picture': 'bla'}
    resp = client.post(reverse('voluntariat:create'), eventx)
    assert (resp.status_code == 200)
    resp1 = client.get(reverse('voluntariat:dashboard'))
    assert len(resp1.context['my_event_list']) == 0


def test_delete(client, event, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.count() == 1)
    getResponse = client.get(reverse('voluntariat:event-delete', kwargs={'pk': 2}))
    assert getResponse.status_code == 200
    resp = client.post(reverse('voluntariat:event-delete', kwargs={'pk': 2}))
    assert (Event.objects.count() == 0)
    assert resp.status_code == 302


def test_delete_fail(client, event, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.count() == 1)
    resp = client.post(reverse('voluntariat:event-delete', kwargs={'pk': 100}))
    assert (Event.objects.count() == 1)
    assert resp.status_code == 404


def test_update(client, event, event3, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    resp = client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.filter(name='Denis').exists() == True)
    responseGet = client.get(reverse('voluntariat:event-update', kwargs={'pk': 4}), event)
    assert responseGet.status_code == 200
    assert responseGet.status_code == 200
    responseq = client.post(reverse('voluntariat:event-update', kwargs={'pk': 4}), {'picture': 'bla'})
    assert (responseq.status_code == 200)
    respUpdated = client.post(reverse('voluntariat:event-update', kwargs={'pk': 4}), event3)
    assert (Event.objects.filter(name='Denis').exists() == False)
    assert (Event.objects.filter(name='Roland').exists() == True)
    assert (respUpdated.status_code == 302)


def test_update_wrongId(client, event, event3, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    resp = client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.filter(name='Denis').exists() == True)

    respUpdated = client.post(reverse('voluntariat:event-update', kwargs={'pk': 1000}), event3)
    assert (Event.objects.filter(name='Denis').exists() == True)
    assert (Event.objects.filter(name='Roland').exists() == False)


def test_my_events(client, event, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    resp = client.get(reverse('voluntariat:myevents'))
    assert len(resp.context['my_event_list']) == 1
    User.objects.create_user(username="user3", password="123456")
    client.logout()
    client.login(username="user3", password="123456")
    resp1 = client.get(reverse('voluntariat:myevents'))
    assert len(resp1.context['my_event_list']) == 0
    resp2 = client.get(reverse('voluntariat:dashboard'))
    assert len(resp2.context['my_event_list']) == 1


def test_see_events(client, event, event2, event3, db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    client.post(reverse('voluntariat:create'), event2)
    client.post(reverse('voluntariat:create'), event3)
    client.logout()
    resp = client.get(reverse('voluntariat:dashboard'))
    assert len(resp.context['my_event_list']) == 3


def test_attend_event(client, user_instance, event_instance):
    client.force_login(user_instance)
    lungime = len(Participantion.objects.all())
    assert lungime == 0

    client.post(reverse('voluntariat:event-attend', kwargs={'pk': event_instance.pk}))
    assert len(Participantion.objects.all()) == 1
    client.logout()

def test_unattend_event(client, user_instance, event_instance):
    client.force_login(user_instance)
    client.post(reverse('voluntariat:event-attend', kwargs={'pk': event_instance.pk}))
    lungime = len(Participantion.objects.all())
    assert lungime == 1

    client.post(reverse('voluntariat:event-unattend', kwargs={'pk': event_instance.pk}))
    assert len(Participantion.objects.all()) == 0
    client.logout()

def test_attend_event_fail( client, user_instance, event_instance):
    client.force_login(user_instance)
    resp = client.get(reverse('voluntariat:event-attend', kwargs={'pk': event_instance.pk}))
    assert len(Participantion.objects.all()) == 0
    client.logout()

def test_unattend_event_fail( client, user_instance, event_instance):
    client.force_login(user_instance)
    resp = client.get(reverse('voluntariat:event-unattend', kwargs={'pk': event_instance.pk}))
    assert len(Participantion.objects.all()) == 0
    client.logout()

def test_can_attend_event_no_user(client, user_instance, event_instance):

    resp = client.get(reverse('voluntariat:event-detail', kwargs={'pk': event_instance.pk}))
    assert b'Pentru a participa la acest eveniment va rugam sa va logati' in resp.content

def test_can_attend_event(client,  event_instance,user_instance2):
    client.force_login(user_instance2)
    resp = client.get(reverse('voluntariat:event-detail', kwargs={'pk': event_instance.pk}))
    assert b'Attend' in resp.content
    client.logout()

def test_can_unattend_event(client,  event_instance,user_instance2):
    participation = Participantion(voluntar=user_instance2, event=event_instance, rating=1, feedback='')
    participation.save()
    client.force_login(user_instance2)
    resp = client.get(reverse('voluntariat:event-detail', kwargs={'pk': event_instance.pk}))
    assert b'Unattend' in resp.content
    client.logout()





