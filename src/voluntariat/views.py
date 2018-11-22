from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader


def login(request):
    page_content = loader.get_template('login.html').render()
    template = loader.get_template('index.html')
    context = {
        'page_content': page_content,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    page_content = "Pagina principala"
    template = loader.get_template('index.html')
    context = {
        'page_content': page_content,
    }
    return HttpResponse(template.render(context, request))

