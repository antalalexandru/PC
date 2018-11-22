from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader


def login(request):
    page_content = loader.get_template('login.html').render()
    return globalTemplate(request, page_content)

def index(request):
    return globalTemplate(request, "Pagina principala")

def globalTemplate(request, page_content):
    template = loader.get_template('index.html')
    context = {
        'page_content': page_content,
    }
    return HttpResponse(template.render(context, request))
    pass

