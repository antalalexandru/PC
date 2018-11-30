from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from django.views import generic
from .forms import EventForm
from django.urls import reverse

class EventListView(generic.ListView):

    model = Event
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("search", None)
        set = Event.objects.all()
        if query is not None:
            set = set.filter(name__icontains=query) | set.filter(description__icontains=query) | set.filter(
                benefits__icontains=query)
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
        if query is not None:
            list = list.filter(name__icontains=query) | list.filter(description__icontains=query) | list.filter(
                benefits__icontains=query)
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
            return redirect(reverse('event-detail', kwargs={'pk': event.pk}))

    else:
        form = EventForm()

    context = {
        'form': form,

    }
    return render(request, 'voluntariat/event_create.html', context)


def event_update_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES,instance=event)
        if form.is_valid():
            event = form.save(commit=False)

            event.organizer = request.user
            event.save()
            return redirect(reverse('event-detail', kwargs={'pk': event.pk}))


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
        return redirect('../../')
    context = {
        "event": obj
    }
    return render(request, "voluntariat/delete.html", context)