import datetime
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
    qs = Article.objects.filter(publish__lte=timezone.now()).order_by('-publish')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 8)
    article_count = paginator.count
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        "articles": articles,
        "article_count": article_count
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

