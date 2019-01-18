import json
import uuid

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from voluntariat import models
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from ..forms import EventForm, LoginForm, SignUpForm, UserForm, ChangePasswordForm, FeedbackForm
from ..models import Event, User, Participantion
from django.db.models import Count


class EventListView(generic.ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("search", None)
        set = Event.objects.all()
        return set

    context_object_name = 'my_event_list'

    queryset = Event.objects.all()
    template_name = "voluntariat/eventlist.html"


class MyEventListView(generic.ListView):
    model = Event
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("query", None)
        list = Event.objects.filter(organizer=self.request.user)
        return list

    context_object_name = 'my_event_list'
    queryset = Event.objects.all()
    template_name = "voluntariat/myeventlist.html"


class UserListView(generic.ListView):
    model = User
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("input",None)
        list = User.objects.exclude(first_name__exact='')
        list =list.exclude(pk=self.request.user.pk)
        if query is not None:
            list= list.filter(Q(first_name__icontains=query) | Q(first_name__icontains=query) | Q(email__icontains=query))
        list=list.annotate(participari= Count('participations')).order_by('-participari')
        return list

    context_object_name = 'user_list'
    queryset = User.objects.all()
    template_name = "voluntariat/userlist.html"


def event_detail_view(request, pk):
    template_name = "voluntariat/my_event_detail.html"
    event = get_object_or_404(Event, pk=pk)
    context={}
    context['event'] = event
    is_participant = len(Participantion.objects.filter(voluntar=request.user.pk, event=event))
    context['is_participant'] =  is_participant
    # context['form'] = FeedbackForm()
    medie = 0
    participantions = Participantion.objects.filter(event=event)
    for part in participantions:
        medie += part.rating
    if len(participantions):
        medie = medie / len(participantions)

    context['medie'] = medie
    if is_participant:
        participation = Participantion.objects.get(event=event.pk, voluntar=request.user.pk)
        if request.method == "POST":
            form = FeedbackForm(request.POST)
            if form.is_valid():
                participation.feedback = form.cleaned_data['comment']
                participation.save()
                return redirect(reverse('voluntariat:event-detail', kwargs={'pk': event.pk}))
        else:
            form = FeedbackForm(initial={'comment': participation.feedback})
        context['form'] = form

    context['participantions'] = participantions

    if event.requested_donation == 0:
        request.donation_percentage = -1
    else:
        donation_percentage = event.accumulated_donation / event.requested_donation
        if donation_percentage >= 1:
            donation_percentage = 100
        else:
            donation_percentage *= 100
        request.donation_percentage = donation_percentage

    if request.user.id is None and models.Event.objects.filter(id=pk)[0].can_add_participants is True:
        request.can_attend = 2
    elif len(models.Event.objects.filter(organizer=request.user.id, id=pk)) != 0 :
        request.can_attend = 3
    elif len(models.Participantion.objects.filter(voluntar_id=request.user.id,
                                                event_id=pk)) == 0 and len(
        models.Event.objects.filter(organizer=request.user.id, pk=pk)) == 0 and models.Event.objects.filter(pk=pk)[0].can_add_participants is True:
        request.can_attend = 1
    elif len(models.Participantion.objects.filter(voluntar_id=request.user.id,
                                                event_id=pk)) == 0 and len(
        models.Event.objects.filter(organizer=request.user.id, id=pk)) == 0 and models.Event.objects.filter(id=pk)[0].can_add_participants is False:
        request.can_attend = 4
    else:
        # len(models.Participantion.objects.filter(voluntar_id=self.request.user.id,
        #                                           event_id=self.kwargs['pk'])) != 0 and len(
        # models.Event.objects.filter(organizer=self.request.user.id, id=self.kwargs['pk'])) == 0:
        request.can_attend = 0

    return render(request, template_name, context)


def eventCreateView(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user

            # save Sendbird group url
            event.send_bird_channel_url = str(uuid.uuid4())
            event.save()

            # create Sendbird channel for the event
            headers = settings.API_TOKEN_CHAT
            data = json.dumps({
                'name': event.name,
                'channel_url': event.send_bird_channel_url,
                'is_public': True,
            })
            requests.post('https://api.sendbird.com/v3/group_channels', headers=headers, data=data)

            # add the event manager to the channel
            data = json.dumps({'user_id': request.user.sendbird_user_id})
            requests.put('https://api.sendbird.com/v3/group_channels/' + event.send_bird_channel_url + '/join', headers=headers, data=data)

            # send create message
            data = json.dumps({
                'message_type': 'MESG',
                'user_id': request.user.sendbird_user_id,
                'message': request.user.username + " created the channel",
            })
            requests.post('https://api.sendbird.com/v3/group_channels/' + event.send_bird_channel_url + '/messages',
                          headers=headers, data=data)

            return redirect(reverse('voluntariat:event-detail', kwargs={'pk': event.pk}))

    else:
        form = EventForm()

    context = {
        'form': form,

    }
    return render(request, 'voluntariat/event_create.html', context)


def event_update_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect(reverse('voluntariat:event-detail', kwargs={'pk': event.pk}))
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'voluntariat/event_update.html', context)


def event_delete_view(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect(reverse('voluntariat:dashboard'))
    context = {
        "event": obj
    }
    return render(request, "voluntariat/delete.html", context)


# this should require login?
def event_attend_view(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        participation = models.Participantion(voluntar=request.user, event=obj, rating=1, feedback='')
        participation.save()

        # add user to channel
        headers = settings.API_TOKEN_CHAT
        data = json.dumps({'user_id': request.user.sendbird_user_id})
        requests.put('https://api.sendbird.com/v3/group_channels/' + obj.send_bird_channel_url + '/join', headers=headers, data=data)

        # send welcome message
        data = json.dumps({
            'message_type': 'MESG',
            'user_id': request.user.sendbird_user_id,
            'message': request.user.username + " joined the channel",
        })
        requests.post('https://api.sendbird.com/v3/group_channels/' + obj.send_bird_channel_url + '/messages',
                     headers=headers, data=data)

        return redirect(reverse('voluntariat:dashboard'))

    context = {
        "event": obj
    }
    return render(request, "voluntariat/attend.html", context)


# this should require login?
def event_unattend_view(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        user = models.User.objects.get(username=request.user.username)
        participation = models.Participantion.objects.filter(voluntar=user, event=obj)
        participation.delete()

        # remove user from channel
        headers = settings.API_TOKEN_CHAT
        data = json.dumps({'user_ids': [request.user.sendbird_user_id]})
        requests.put('https://api.sendbird.com/v3/group_channels/' + obj.send_bird_channel_url + '/leave', headers=headers, data=data)

        return redirect(reverse('voluntariat:dashboard'))

    context = {
        "event": obj
    }
    return render(request, "voluntariat/unattend.html", context)

@login_required
def event_stop_attendings_view(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        obj.can_add_participants = False
        obj.save(update_fields=['can_add_participants'])

        return redirect(reverse('voluntariat:dashboard'))

    context = {
        "event": obj
    }
    return render(request, "voluntariat/stop_attendings.html", context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('voluntariat:dashboard')
            else:
                return render(request, 'voluntariat/login.html', {
                    'message': 'Invalid credentials',
                    'form': LoginForm()
                }, status=400)

    return render(request, 'voluntariat/login.html', {'form': LoginForm()})


@login_required
def my_profile(request):
    context = {"user": request.user}
    return render(request, 'voluntariat/myprofile.html', context)


def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'voluntariat/userprofile.html', {'user': user})

@login_required
def my_profile_update(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(reverse('voluntariat:myprofile'))

    else:
        form = UserForm(instance=user)
    return render(request, 'voluntariat/myprofile_update.html', {'form': form, 'user': user})


@login_required
def my_profile_change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        old_password = request.POST.get("old_password")
        if not user.check_password(old_password):
            form.set_old_password_flag()
        if form.is_valid():
            new_password = form.clean().get('new_password')
            user.set_password(new_password)
            user.save()
            login(request, user)
            return redirect(reverse('voluntariat:myprofile'))
    else:
        form = ChangePasswordForm()

    return render(request, 'voluntariat/myprofile_change_password.html', {'form': form, 'user': user})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # create Sendbird user based on secure hash
            user.sendbird_user_id = str(uuid.uuid4())
            user.save()
            headers = settings.API_TOKEN_CHAT
            data = json.dumps({
                'user_id': user.sendbird_user_id,
                'nickname': user.username,
                'profile_url': '',
            })
            requests.post('https://api.sendbird.com/v3/users', headers=headers, data=data)

            return redirect('voluntariat:dashboard')
    else:
        form = SignUpForm()

    return render(request, 'voluntariat/signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('voluntariat:dashboard')

@csrf_exempt
def update_rate(request):
    if request.method == 'POST':
        value= request.POST.get('value')
        pk = request.POST.get('pk')
        pk2 = request.POST.get('pk2')
        participation = Participantion.objects.get(event=pk, voluntar=pk2)
        participation.rating = value
        participation.save()
        return HttpResponse('ok')
