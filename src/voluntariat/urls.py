
from django.urls import path

from voluntariat.views.generic_views import update_rate
from .views import generic_views, chat_views, stripe_views

app_name = 'voluntariat'


urlpatterns = [
    path('', generic_views.EventListView.as_view(), name='dashboard'),
    path('login/', generic_views.login_view, name='login'),
    path('signup/', generic_views.signup, name='signup'),
    path('logout/', generic_views.logout_view, name='logout'),
    path('myevents/', generic_views.MyEventListView.as_view(), name='myevents'),
    path('create/', generic_views.eventCreateView, name='create'),
    path('event/<int:pk>/', generic_views.event_detail_view, name='event-detail'),
    path('event/<int:pk>/delete/', generic_views.event_delete_view, name='event-delete'),
    path('event/<int:pk>/update/', generic_views.event_update_view, name='event-update'),
    path('event/<int:pk>/attend/', generic_views.event_attend_view, name='event-attend'),
    path('event/<int:pk>/unattend/', generic_views.event_unattend_view, name='event-unattend'),
    path('event/<int:pk>/stopAttendings/', generic_views.event_stop_attendings_view, name='event-stop-attendings'),
    path('myprofile/', generic_views.my_profile, name='myprofile'),
    path('myprofile/update/', generic_views.my_profile_update, name="myprofile-update"),
    path('myprofile/changePassword/', generic_views.my_profile_change_password, name="myprofile-change-password"),
    path('chat/', chat_views.chat, name='chat'),
    path('chat/index.html', chat_views.chat_index, name='chat_index'),
    path('stripe/', stripe_views.stripe_connect, name='stripe'),
    path('checkout', stripe_views.stripe_checkout, name='checkout'),
    path('userlist/', generic_views.UserListView.as_view(), name='userlist'),
    path('userprofile/<int:id>/',generic_views.user_profile,name='userprofile'),
    path('volunteers/', generic_views.volunteers_list, name='volunteers'),
    path('volunteers/<int:pk>/send/', generic_views.volunteer_send_email, name='volunteer-send'),
    path('update_rate/',update_rate,name='update_rate'),
    path('event/<int:pk>/list/', generic_views.MyUserListView.as_view(), name='event-list'),
    path('block/<int:id>/', generic_views.block_user, name='event-block'),

]
