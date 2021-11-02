from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import EventForm
from.models import Event, User

# Create your views here.

@permission_required('events.view_event')
def event_list_view(request):
    qs = Event.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "events/list.html", context)
