import pytest
from voluntariat.models import Event,User
from django.urls import reverse
from voluntariat.forms import EventForm
from django.db import models
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock
from django.core.files import File
import tempfile


@pytest.fixture
def event(request,db):
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
def event2(request,db):
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
def event3(request,db):
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


def test_add(client,event,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    resp = client.post(reverse('voluntariat:create'), event)
    assert Event.objects.filter(name='Denis').exists()

    assert (resp.status_code==302)
    resp1 = client.get(reverse('voluntariat:dashboard'))

    assert len(resp1.context['my_event_list']) == 1
    responseGet=client.get(reverse('voluntariat:create'),event)
    assert responseGet.status_code==200


def test_add_fail(client,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username,password=password)

    eventx={'picture':'bla'}
    resp=client.post(reverse('voluntariat:create'),eventx)
    assert (resp.status_code==200)
    resp1 = client.get(reverse('voluntariat:dashboard'))
    assert len(resp1.context['my_event_list']) == 0

def test_delete(client,event,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.count()==1)
    getResponse =client.get(reverse('voluntariat:event-delete', kwargs={'pk':2}))
    assert getResponse.status_code==200
    resp=client.post(reverse('voluntariat:event-delete', kwargs={'pk':2}))
    assert (Event.objects.count() == 0)
    assert resp.status_code==302




def test_delete_fail(client,event,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.count() == 1)
    resp = client.post(reverse('voluntariat:event-delete', kwargs={'pk': 100}))
    assert (Event.objects.count() == 1)
    assert resp.status_code == 404



def test_update(client,event,event3,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    resp = client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.filter(name='Denis').exists() == True)
    responseGet = client.get(reverse('voluntariat:event-update', kwargs={'pk': 4}), event)
    assert responseGet.status_code == 200
    assert responseGet.status_code == 200
    responseq = client.post(reverse('voluntariat:event-update', kwargs={'pk': 4}), {'picture':'bla'})
    assert (responseq.status_code==200)
    respUpdated=client.post(reverse('voluntariat:event-update',kwargs={'pk': 4}),event3)
    assert (Event.objects.filter(name='Denis').exists() == False)
    assert (Event.objects.filter(name='Roland').exists() == True)
    assert(respUpdated.status_code==302)


def test_update_wrongId(client,event,event3,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    resp = client.post(reverse('voluntariat:create'), event)
    assert (Event.objects.filter(name='Denis').exists() == True)

    respUpdated=client.post(reverse('voluntariat:event-update',kwargs={'pk': 1000}),event3)
    assert (Event.objects.filter(name='Denis').exists() == True)
    assert (Event.objects.filter(name='Roland').exists() == False)


def test_my_events(client,event,db):
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
    resp1=client.get(reverse('voluntariat:myevents'))
    assert len(resp1.context['my_event_list']) == 0
    resp2 = client.get(reverse('voluntariat:dashboard'))
    assert len(resp2.context['my_event_list']) == 1


def test_see_events(client,event,event2,event3,db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    client.post(reverse('voluntariat:create'), event)
    client.post(reverse('voluntariat:create'), event2)
    client.post(reverse('voluntariat:create'), event3)
    client.logout()
    resp=client.get(reverse('voluntariat:dashboard'))
    assert len(resp.context['my_event_list']) == 3




