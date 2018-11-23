from django.urls import path
from . import  views
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    path('', views.EventListView.as_view(), name='event'),
    path('myevents/', views.MyEventListView.as_view(), name='myevents'),
    path('create/', views.eventCreateView, name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('<int:pk>/delete/', views.event_delete_view, name='event-delete'),
path('<int:pk>/update/', views.event_update_view, name='event-update'),
]