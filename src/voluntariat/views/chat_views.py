from django.shortcuts import render


def chat(request):
    return render(request, 'voluntariat/chat/chat.html')


def chat_index(request):
    return render(request, 'voluntariat/chat/index.html')
