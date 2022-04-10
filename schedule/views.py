from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Typical
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User

# Create your views here.

@permission_required('schedule.change_typical')
def schedule_list_view(request):
    requesting_user = request.user
    if requesting_user.has_perms('schedule.change_typical'):
        qs = Typical.objects.filter(active=True).order_by('user')
        howmany = 2
    else:
        qs = Typical.objects.filter(active=True, user=requesting_user)
        howmany = None

    add_missing_schedules = None

    qs1 = User.objects.filter(is_active=True)
    for each in qs1:
        try:
            qs2 = Typical.objects.get(user=each)
        except:
            print('Identified Missing Users')
            add_missing_schedules = True

    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 20)

    schedule_count = paginator.count
    try:
        schedules = paginator.page(page)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    context = {
        "schedules": schedules,
        "add_missing_schedules": add_missing_schedules,
        "howmany": howmany,
        "schedule_count": schedule_count,
    }
    return render(request, "schedule/list.html", context)


@permission_required('schedule.view_typical')
def schedule__staff_view(request):
    requesting_user = request.user
    qs = Typical.objects.filter(active=True, user=requesting_user).order_by('user')
    howmany = None

    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 20)

    schedule_count = paginator.count
    try:
        schedules = paginator.page(page)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    context = {
        "schedules": schedules,
        "howmany": howmany,
        "schedule_count": schedule_count,
    }
    return render(request, "schedule/list.html", context)


@permission_required('schedule.add_typical')
def schedule_create_view(request):
    qs1 = User.objects.filter(is_active=True)
    for each in qs1:
        try:
            qs2 = Typical.objects.get(user=each)
            print('User Schedule Exists')
        except:
            Typical.objects.create(user=each)
            print('User Schedule Created')

    qs = Typical.objects.filter(active=True).order_by('user')
    howmany = 2

    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 20)

    schedule_count = paginator.count
    try:
        schedules = paginator.page(page)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    context = {
        "schedules": schedules,
        "howmany": howmany,
        "schedule_count": schedule_count,
    }
    return render(request, "schedule/list.html", context)
