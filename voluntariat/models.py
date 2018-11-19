from django.contrib.auth.models import AbstractUser
from django.db import models


class Event(models.Model):
    organizer = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    piture = models.ImageField(upload_to='event_pics/%Y/%m/%d')
    location = models.CharField(max_length=100)
    description = models.TextField()
    benefits = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    send_bird_channel_url = models.CharField(max_length=100)


class User(AbstractUser):
    email = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    age = models.IntegerField()
    personal_description = models.TextField()

    stripe_client_id = models.CharField(max_length=1000)
    stripe_customer_id = models.CharField(max_length=1000)
    sendbird_user_id = models.CharField(max_length=1000)

    participations = models.ManyToManyField(Event, through='Participantion')


class Participantion(models.Model):
    voluntar = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.FloatField()
    stripe_charge_id = models.CharField(max_length=1000)
