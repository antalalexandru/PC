import json

import requests
from django.shortcuts import render
from requests.auth import HTTPDigestAuth

from src.PC import settings


def stripe(request):
    headers = settings.API_TOKEN_STRIPE
    res = requests.get('https://api.stripe.com/v1/balance', headers=headers)

    return render(request, 'voluntariat/stripe/stripe.html')
