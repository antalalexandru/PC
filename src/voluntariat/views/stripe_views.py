import json
import stripe
import requests

# Required for OAuth flow
from rauth import OAuth2Service

from django.shortcuts import render

from django.conf import settings

from ..models import User


def stripe(request):
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
    connect_access_token = stripe_payload['access_token']

    request.user.stripe_client_id = connect_access_token
    request.user.save()

    return render(request, 'voluntariat/stripe/stripe.html')
