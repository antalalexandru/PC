import json
import stripe
import requests

# Required for OAuth flow
from django.urls import reverse
from rauth import OAuth2Service

from django.shortcuts import render, redirect

from django.conf import settings

from ..models import User, Event

stripe.api_key = settings.API_TOKEN_STRIPE


def stripe_connect(request):
    # Set up your OAuth flow parameters
    stripe_connect_service = OAuth2Service(
        name='stripe',
        client_id=settings.CLIENT_TOKEN_STRIPE,
        client_secret=settings.API_TOKEN_STRIPE,
        authorize_url='https://connect.stripe.com/oauth/authorize',
        access_token_url='https://connect.stripe.com/oauth/token',
        base_url='https://api.stripe.com/',
    )

    # They return to your site from filling out a form on stripe and...
    # There's a temporary code returned when they're redirected to your site.
    # In Django, you would grab it like this
    code = request.GET.get('code', '')
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }

    # Use your OAuth service to get a response
    resp = stripe_connect_service.get_raw_access_token(method='POST', data=data)

    # They returned JSON
    stripe_payload = json.loads(resp.text)
    print(stripe_payload)

    # They return four parameters.  We only care about the 'access_token' right now
    connect_access_token = stripe_payload['stripe_user_id']

    request.user.stripe_client_id = connect_access_token
    request.user.save()

    return render(request, 'voluntariat/stripe/stripe.html')


def stripe_checkout(request):
    if request.method == "POST":
        token = request.POST.get("stripeToken")
        event_id = int(request.POST.get("event_id"))
        event = Event.objects.get(id=event_id)

    stripe.Charge.create(
        amount=999,
        currency="ron",
        source=token,
        description="Ai donat 10 lei",
        stripe_account="acct_1Dr3OXJxau59OLf7",
    )

    event.accumulated_donation += 10
    event.save()

    return redirect(reverse('voluntariat:event-detail', kwargs={'pk': event_id}))
