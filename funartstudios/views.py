from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render
from django.utils import timezone
from articles.models import Article
from events.models import Event

@login_required
def home_view(request, *args, **kwargs):
    queryset = Article.objects.filter(publish__lt=timezone.now()).order_by('-publish')
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

