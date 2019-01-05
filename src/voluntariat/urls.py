from django.urls import path

from . import views

app_name = 'voluntariat'

urlpatterns = [
    path('', views.EventListView.as_view(), name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('myevents/', views.MyEventListView.as_view(), name='myevents'),
    path('create/', views.eventCreateView, name='create'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/delete/', views.event_delete_view, name='event-delete'),
    path('event/<int:pk>/update/', views.event_update_view, name='event-update'),
    path('event/<int:pk>/attend/', views.event_attend_view, name='event-attend'),
    path('event/<int:pk>/unattend/', views.event_unattend_view, name='event-unattend'),
    path('myprofile/', views.my_profile, name='myprofile'),
    path('myprofile/update/', views.my_profile_update, name="myprofile-update"),
    path('myprofile/changePassword/', views.my_profile_change_password, name="myprofile-change-password")
]
