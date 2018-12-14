from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, User
from django.views import generic
from .forms import EventForm, LoginForm, SignUpForm
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q


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


def logout_view(request):
    logout(request)
    return redirect('voluntariat:dashboard')


def volunteers_list(request, q=None):
    user_list = User.objects.all()

    query = q or request.GET.get('q')
    if query:
        user_list = user_list.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(username__icontains=query)
        ).distinct()

    paginator = Paginator(user_list, 2)

    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'voluntariat/volunteerslist.html', context={'users': users, 'q': query})


def volunteer_send_email(request, pk):
    obj = User.objects.get(pk=pk)
    if request.method == "POST":
        email = EmailMessage('Invitatie', 'Invitatie pentru urmatorul eveniment: linkattend', to=[obj.email])
        email.send()
        return redirect(reverse('voluntariat:volunteers'))
    context = {"user": obj}
    return render(request, "voluntariat/send_em.html", context)
