import pytest
from voluntariat.models import Event, User, Participantion
from django.urls import reverse
from datetime import datetime


def test_see_users(client,  db):
    username = "user1"
    password = "bar"
    User.objects.create_user(username=username,first_name='Denis' ,password=password)
    User.objects.create_user(username="user2", first_name='B' ,password="bar")
    User.objects.create_user(username="user3",first_name='Irvine' , password="bar")
    client.login(username=username, password=password)
    resp = client.get(reverse('voluntariat:userlist'))
    assert len(resp.context['user_list']) == 2
    client.logout()
    resp = client.get(reverse('voluntariat:userlist'))
    assert len(resp.context['user_list']) == 3
    resp = client.get('%s?input=Irv' % reverse('voluntariat:userlist'))
    assert len(resp.context['user_list']) == 1

def test_see_userprofile(client,db):
    User.objects.create_user(username="user1", first_name='Denis', password="bar")
    User.objects.create_user(username="user2", first_name='B', password="bar")
    User.objects.create_user(username="user3", first_name='Irvine', password="bar")
    user = User.objects.get(username="user1")
    resp=client.get(reverse('voluntariat:userprofile',kwargs={'id': user.pk}))
    assert resp.status_code == 200