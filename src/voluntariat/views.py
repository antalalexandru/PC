from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from .forms import EventForm, LoginForm, SignUpForm, UserForm, ChangePasswordForm
from .models import Event, User


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


class EventDetailView(generic.DetailView):
    model = Event
    template_name = "voluntariat/my_event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        donation_percentage = event.accumulated_donation / event.requested_donation
        if donation_percentage >= 1:
            donation_percentage = 100
        else:
            donation_percentage *= 100
        self.request.donation_percentage = donation_percentage
        return context


def eventCreateView(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
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
            return redirect('voluntariat:dashboard')
        else:
            return render(request, 'voluntariat/signup.html', {'form': SignUpForm()}, status=400)
    else:
        return render(request, 'voluntariat/signup.html', {'form': SignUpForm()})

@login_required
def logout_view(request):
    logout(request)
    return redirect('voluntariat:dashboard')
