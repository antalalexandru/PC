import pytest
from django.urls import reverse
from unittest import mock
from voluntariat.models import User


def fake_send(self, fail_silently=False):
    """Send the email message."""
    pass


def test_see_users(client, db):
    User.objects.create_user(username='Ana', password='password')
    User.objects.create_user(username='username2', password='password2')
    User.objects.create_user(username='username3', password='password3')
    resp = client.get(f'{reverse("voluntariat:volunteers")}?q=Ana')
    assert len(resp.context['users'].object_list) == 1

    resp = client.get(f'{reverse("voluntariat:volunteers")}')
    assert len(resp.context['users'].object_list) == 3


def test_send_email(client, db):
    user = User.objects.create_user(username='username', password='password')
    with mock.patch('django.core.mail.message.EmailMessage.send', fake_send):
        resp = client.post(reverse("voluntariat:volunteer-send", kwargs={'pk': user.pk}))
        assert resp.status_code == 302


def test_get_object(client, db):
    user = User.objects.create_user(username='username', password='password')
    resp = client.get(reverse("voluntariat:volunteer-send", kwargs={'pk': user.pk}))
    assert resp.context['user'].pk == user.pk