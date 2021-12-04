import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render
from django.utils import timezone
from articles.models import Article, Comment
from events.models import Event 
from django.db.models import Q

@login_required
def home_view(request, *args, **kwargs): 
    # next_event = Event.objects.filter(date__gte=timezone.now)
    now = timezone.now()
    print(now)
    if request.method == "POST":
        query = request.POST.get('q')
        lookups = Q(title__icontains=query) | Q(content__icontains=query)  
        qs = Article.objects.filter(lookups, publish__lte=timezone.now()).order_by('-publish').distinct()
    else:
        qs = Article.objects.filter(publish__lte=timezone.now()).order_by('-publish')
        query = ''
    page = request.GET.get('page', 1)
    for each in qs:
        comments = Comment.objects.filter(article=each.id).count()
        each.comment = comments
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
        "article_count": article_count,
        "query": query
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

import os

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def github_pull(request):
    if request.method == "POST":
        os.system("sudo /home/ubuntu/.githubpull.sh" )
        return HttpResponse('It Works')
    return HttpResponse('Hello World')
