from django.contrib.auth.decorators import permission_required
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

