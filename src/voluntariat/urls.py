from django.contrib import admin
from django.urls import path, include

from voluntariat import views

app_name = 'voluntariat'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
