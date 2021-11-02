from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from events.models import Event

@login_required
def home_view(request, *args, **kwargs):
    queryset = Event.objects.all().order_by('-date')
    context = {
        "object_list": queryset,
    }
    HTML_STRING = render_to_string('home-view.html', context=context)
    return HttpResponse(HTML_STRING)

