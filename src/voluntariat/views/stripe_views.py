import stripe
from django.shortcuts import render

from src.PC import settings


def stripe(request):
    stripe.api_key = settings.API_TOKEN_STRIPE
    res = stripe.Balance.retrieve()

    return render(request, 'voluntariat/stripe/stripe.html')
