from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from events.models import Event

@permission_required('events.view_event')
def home_view(request, *args, **kwargs):
    queryset = Event.objects.all().order_by('-date')
    context = {
        "object_list": queryset,
    }
    return render(request, 'home-view.html', context)

@permission_required('events.view_event')
def about_view(request, *args, **kwargs):
    qs = Event.objects.all().order_by('-date').exclude(type='i')
    paginator = Paginator(qs, 10)
    event_count = paginator.count
    context = {
        "user": request.user,
        "event_count": event_count

    }
    return render(request, 'about-view.html', context)

