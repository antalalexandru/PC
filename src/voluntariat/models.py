
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Event(models.Model):
    organizer = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='event_pics/%Y/%m/%d', max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField()
    benefits = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    send_bird_channel_url = models.CharField(max_length=100, default='default')
    can_add_participants = models.BooleanField(default=True)

    requested_donation = models.PositiveIntegerField(default=0)
    accumulated_donation = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('voluntariat:event-detail', args=[str(self.id)])


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, validators=[MinLengthValidator(8)])
    email = models.EmailField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    age = models.IntegerField(default=30)
    personal_description = models.TextField()
    picture = models.ImageField(upload_to='profile_images', default='git_images/default-profile.jpg', max_length=255)

    stripe_client_id = models.CharField(max_length=1000)
    stripe_customer_id = models.CharField(max_length=1000)
    sendbird_user_id = models.CharField(max_length=1000)

    participations = models.ManyToManyField(Event, through='Participantion')


class Participantion(models.Model):
    voluntar = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.FloatField()
    feedback = models.TextField(null=True)
    blocked = models.BooleanField(default=False)


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.FloatField()
    stripe_charge_id = models.CharField(max_length=1000)


