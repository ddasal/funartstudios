from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from .models import ScheduleChange, Typical, TimeOffRequest
from .forms import TimeOffForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from django.http.response import Http404
import datetime
from django.db import IntegrityError


# Create your views here.

@permission_required('schedule.change_typical')
def schedule_list_view(request):
    qs = Typical.objects.filter(active=True).order_by('user')
    today = datetime.date.today()
    existing = TimeOffRequest.objects.filter(active=True, end_date__gte=today).order_by('start_date')
    howmany = 2

    add_missing_schedules = None

    qs1 = User.objects.filter(is_active=True)
    for each in qs1:
        try:
            qs2 = Typical.objects.get(user=each)
        except:
            print('Identified Missing Users')
            add_missing_schedules = True

    for each in qs:
        try:
            qs3 = ScheduleChange.objects.get(user=each.user)
            each.pending = 'y'
            each.pending_id = qs3.id
            print('pending')
        except:
            pass


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
        "existing": existing
    }
    return render(request, "schedule/list.html", context)


@permission_required('schedule.view_typical')
def schedule_staff_view(request):
    requesting_user = request.user
    qs = Typical.objects.filter(active=True, user=requesting_user).order_by('user')
    existing = TimeOffRequest.objects.filter(active=True, user=request.user).order_by('start_date')

    try:
        qs2 = ScheduleChange.objects.get(active=True, user=requesting_user)
        if qs2:
            status = qs2.get_status_display
    except:
        status = None
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
        "status": status,
        "schedule_count": schedule_count,
        "existing": existing
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


@permission_required('schedule.add_schedulechange')
def schedule_staff_edit_view(request):
    requesting_user = request.user

    if request.method == 'POST':

        if request.POST.get('status') == 'new':
            print('new request')
            message = 'Your new request has been subbmited'

            ScheduleChange.objects.create(user=requesting_user)
            obj = ScheduleChange.objects.get(user=requesting_user)

            obj.start_date = request.POST.get('start_date')

            if request.POST.get('monday_8am') == 'on':
                obj.monday_8am = True
            else:
                obj.monday_8am = False
            if request.POST.get('monday_9am') == 'on':
                obj.monday_9am = True
            else:
                obj.monday_9am = False
            if request.POST.get('monday_10am') == 'on':
                obj.monday_10am = True
            else:
                obj.monday_10am = False
            if request.POST.get('monday_11am') == 'on':
                obj.monday_11am = True
            else:
                obj.monday_11am = False
            if request.POST.get('monday_12pm') == 'on':
                obj.monday_12pm = True
            else:
                obj.monday_12pm = False
            if request.POST.get('monday_1pm') == 'on':
                obj.monday_1pm = True
            else:
                obj.monday_1pm = False
            if request.POST.get('monday_2pm') == 'on':
                obj.monday_2pm = True
            else:
                obj.monday_2pm = False
            if request.POST.get('monday_3pm') == 'on':
                obj.monday_3pm = True
            else:
                obj.monday_3pm = False
            if request.POST.get('monday_4pm') == 'on':
                obj.monday_4pm = True
            else:
                obj.monday_4pm = False
            if request.POST.get('monday_5pm') == 'on':
                obj.monday_5pm = True
            else:
                obj.monday_5pm = False
            if request.POST.get('monday_6pm') == 'on':
                obj.monday_6pm = True
            else:
                obj.monday_6pm = False
            if request.POST.get('monday_7pm') == 'on':
                obj.monday_7pm = True
            else:
                obj.monday_7pm = False
            if request.POST.get('monday_8pm') == 'on':
                obj.monday_8pm = True
            else:
                obj.monday_8pm = False
            if request.POST.get('monday_9pm') == 'on':
                obj.monday_9pm = True
            else:
                obj.monday_9pm = False
            if request.POST.get('monday_10pm') == 'on':
                obj.monday_10pm = True
            else:
                obj.monday_10pm = False

            obj.monday_recurrence =  request.POST.get('monday_recurrence')


            if request.POST.get('tuesday_8am') == 'on':
                obj.tuesday_8am = True
            else:
                obj.tuesday_8am = False
            if request.POST.get('tuesday_9am') == 'on':
                obj.tuesday_9am = True
            else:
                obj.tuesday_9am = False
            if request.POST.get('tuesday_10am') == 'on':
                obj.tuesday_10am = True
            else:
                obj.tuesday_10am = False
            if request.POST.get('tuesday_11am') == 'on':
                obj.tuesday_11am = True
            else:
                obj.tuesday_11am = False
            if request.POST.get('tuesday_12pm') == 'on':
                obj.tuesday_12pm = True
            else:
                obj.tuesday_12pm = False
            if request.POST.get('tuesday_1pm') == 'on':
                obj.tuesday_1pm = True
            else:
                obj.tuesday_1pm = False
            if request.POST.get('tuesday_2pm') == 'on':
                obj.tuesday_2pm = True
            else:
                obj.tuesday_2pm = False
            if request.POST.get('tuesday_3pm') == 'on':
                obj.tuesday_3pm = True
            else:
                obj.tuesday_3pm = False
            if request.POST.get('tuesday_4pm') == 'on':
                obj.tuesday_4pm = True
            else:
                obj.tuesday_4pm = False
            if request.POST.get('tuesday_5pm') == 'on':
                obj.tuesday_5pm = True
            else:
                obj.tuesday_5pm = False
            if request.POST.get('tuesday_6pm') == 'on':
                obj.tuesday_6pm = True
            else:
                obj.tuesday_6pm = False
            if request.POST.get('tuesday_7pm') == 'on':
                obj.tuesday_7pm = True
            else:
                obj.tuesday_7pm = False
            if request.POST.get('tuesday_8pm') == 'on':
                obj.tuesday_8pm = True
            else:
                obj.tuesday_8pm = False
            if request.POST.get('tuesday_9pm') == 'on':
                obj.tuesday_9pm = True
            else:
                obj.tuesday_9pm = False
            if request.POST.get('tuesday_10pm') == 'on':
                obj.tuesday_10pm = True
            else:
                obj.tuesday_10pm = False

            obj.tuesday_recurrence =  request.POST.get('tuesday_recurrence')


            if request.POST.get('wednesday_8am') == 'on':
                obj.wednesday_8am = True
            else:
                obj.wednesday_8am = False
            if request.POST.get('wednesday_9am') == 'on':
                obj.wednesday_9am = True
            else:
                obj.wednesday_9am = False
            if request.POST.get('wednesday_10am') == 'on':
                obj.wednesday_10am = True
            else:
                obj.wednesday_10am = False
            if request.POST.get('wednesday_11am') == 'on':
                obj.wednesday_11am = True
            else:
                obj.wednesday_11am = False
            if request.POST.get('wednesday_12pm') == 'on':
                obj.wednesday_12pm = True
            else:
                obj.wednesday_12pm = False
            if request.POST.get('wednesday_1pm') == 'on':
                obj.wednesday_1pm = True
            else:
                obj.wednesday_1pm = False
            if request.POST.get('wednesday_2pm') == 'on':
                obj.wednesday_2pm = True
            else:
                obj.wednesday_2pm = False
            if request.POST.get('wednesday_3pm') == 'on':
                obj.wednesday_3pm = True
            else:
                obj.wednesday_3pm = False
            if request.POST.get('wednesday_4pm') == 'on':
                obj.wednesday_4pm = True
            else:
                obj.wednesday_4pm = False
            if request.POST.get('wednesday_5pm') == 'on':
                obj.wednesday_5pm = True
            else:
                obj.wednesday_5pm = False
            if request.POST.get('wednesday_6pm') == 'on':
                obj.wednesday_6pm = True
            else:
                obj.wednesday_6pm = False
            if request.POST.get('wednesday_7pm') == 'on':
                obj.wednesday_7pm = True
            else:
                obj.wednesday_7pm = False
            if request.POST.get('wednesday_8pm') == 'on':
                obj.wednesday_8pm = True
            else:
                obj.wednesday_8pm = False
            if request.POST.get('wednesday_9pm') == 'on':
                obj.wednesday_9pm = True
            else:
                obj.wednesday_9pm = False
            if request.POST.get('wednesday_10pm') == 'on':
                obj.wednesday_10pm = True
            else:
                obj.wednesday_10pm = False

            obj.wednesday_recurrence =  request.POST.get('wednesday_recurrence')


            if request.POST.get('thursday_8am') == 'on':
                obj.thursday_8am = True
            else:
                obj.thursday_8am = False
            if request.POST.get('thursday_9am') == 'on':
                obj.thursday_9am = True
            else:
                obj.thursday_9am = False
            if request.POST.get('thursday_10am') == 'on':
                obj.thursday_10am = True
            else:
                obj.thursday_10am = False
            if request.POST.get('thursday_11am') == 'on':
                obj.thursday_11am = True
            else:
                obj.thursday_11am = False
            if request.POST.get('thursday_12pm') == 'on':
                obj.thursday_12pm = True
            else:
                obj.thursday_12pm = False
            if request.POST.get('thursday_1pm') == 'on':
                obj.thursday_1pm = True
            else:
                obj.thursday_1pm = False
            if request.POST.get('thursday_2pm') == 'on':
                obj.thursday_2pm = True
            else:
                obj.thursday_2pm = False
            if request.POST.get('thursday_3pm') == 'on':
                obj.thursday_3pm = True
            else:
                obj.thursday_3pm = False
            if request.POST.get('thursday_4pm') == 'on':
                obj.thursday_4pm = True
            else:
                obj.thursday_4pm = False
            if request.POST.get('thursday_5pm') == 'on':
                obj.thursday_5pm = True
            else:
                obj.thursday_5pm = False
            if request.POST.get('thursday_6pm') == 'on':
                obj.thursday_6pm = True
            else:
                obj.thursday_6pm = False
            if request.POST.get('thursday_7pm') == 'on':
                obj.thursday_7pm = True
            else:
                obj.thursday_7pm = False
            if request.POST.get('thursday_8pm') == 'on':
                obj.thursday_8pm = True
            else:
                obj.thursday_8pm = False
            if request.POST.get('thursday_9pm') == 'on':
                obj.thursday_9pm = True
            else:
                obj.thursday_9pm = False
            if request.POST.get('thursday_10pm') == 'on':
                obj.thursday_10pm = True
            else:
                obj.thursday_10pm = False

            obj.thursday_recurrence =  request.POST.get('thursday_recurrence')


            if request.POST.get('friday_8am') == 'on':
                obj.friday_8am = True
            else:
                obj.friday_8am = False
            if request.POST.get('friday_9am') == 'on':
                obj.friday_9am = True
            else:
                obj.friday_9am = False
            if request.POST.get('friday_10am') == 'on':
                obj.friday_10am = True
            else:
                obj.friday_10am = False
            if request.POST.get('friday_11am') == 'on':
                obj.friday_11am = True
            else:
                obj.friday_11am = False
            if request.POST.get('friday_12pm') == 'on':
                obj.friday_12pm = True
            else:
                obj.friday_12pm = False
            if request.POST.get('friday_1pm') == 'on':
                obj.friday_1pm = True
            else:
                obj.friday_1pm = False
            if request.POST.get('friday_2pm') == 'on':
                obj.friday_2pm = True
            else:
                obj.friday_2pm = False
            if request.POST.get('friday_3pm') == 'on':
                obj.friday_3pm = True
            else:
                obj.friday_3pm = False
            if request.POST.get('friday_4pm') == 'on':
                obj.friday_4pm = True
            else:
                obj.friday_4pm = False
            if request.POST.get('friday_5pm') == 'on':
                obj.friday_5pm = True
            else:
                obj.friday_5pm = False
            if request.POST.get('friday_6pm') == 'on':
                obj.friday_6pm = True
            else:
                obj.friday_6pm = False
            if request.POST.get('friday_7pm') == 'on':
                obj.friday_7pm = True
            else:
                obj.friday_7pm = False
            if request.POST.get('friday_8pm') == 'on':
                obj.friday_8pm = True
            else:
                obj.friday_8pm = False
            if request.POST.get('friday_9pm') == 'on':
                obj.friday_9pm = True
            else:
                obj.friday_9pm = False
            if request.POST.get('friday_10pm') == 'on':
                obj.friday_10pm = True
            else:
                obj.friday_10pm = False

            obj.friday_recurrence =  request.POST.get('friday_recurrence')


            if request.POST.get('saturday_8am') == 'on':
                obj.saturday_8am = True
            else:
                obj.saturday_8am = False
            if request.POST.get('saturday_9am') == 'on':
                obj.saturday_9am = True
            else:
                obj.saturday_9am = False
            if request.POST.get('saturday_10am') == 'on':
                obj.saturday_10am = True
            else:
                obj.saturday_10am = False
            if request.POST.get('saturday_11am') == 'on':
                obj.saturday_11am = True
            else:
                obj.saturday_11am = False
            if request.POST.get('saturday_12pm') == 'on':
                obj.saturday_12pm = True
            else:
                obj.saturday_12pm = False
            if request.POST.get('saturday_1pm') == 'on':
                obj.saturday_1pm = True
            else:
                obj.saturday_1pm = False
            if request.POST.get('saturday_2pm') == 'on':
                obj.saturday_2pm = True
            else:
                obj.saturday_2pm = False
            if request.POST.get('saturday_3pm') == 'on':
                obj.saturday_3pm = True
            else:
                obj.saturday_3pm = False
            if request.POST.get('saturday_4pm') == 'on':
                obj.saturday_4pm = True
            else:
                obj.saturday_4pm = False
            if request.POST.get('saturday_5pm') == 'on':
                obj.saturday_5pm = True
            else:
                obj.saturday_5pm = False
            if request.POST.get('saturday_6pm') == 'on':
                obj.saturday_6pm = True
            else:
                obj.saturday_6pm = False
            if request.POST.get('saturday_7pm') == 'on':
                obj.saturday_7pm = True
            else:
                obj.saturday_7pm = False
            if request.POST.get('saturday_8pm') == 'on':
                obj.saturday_8pm = True
            else:
                obj.saturday_8pm = False
            if request.POST.get('saturday_9pm') == 'on':
                obj.saturday_9pm = True
            else:
                obj.saturday_9pm = False
            if request.POST.get('saturday_10pm') == 'on':
                obj.saturday_10pm = True
            else:
                obj.saturday_10pm = False

            obj.saturday_recurrence =  request.POST.get('saturday_recurrence')


            if request.POST.get('sunday_8am') == 'on':
                obj.sunday_8am = True
            else:
                obj.sunday_8am = False
            if request.POST.get('sunday_9am') == 'on':
                obj.sunday_9am = True
            else:
                obj.sunday_9am = False
            if request.POST.get('sunday_10am') == 'on':
                obj.sunday_10am = True
            else:
                obj.sunday_10am = False
            if request.POST.get('sunday_11am') == 'on':
                obj.sunday_11am = True
            else:
                obj.sunday_11am = False
            if request.POST.get('sunday_12pm') == 'on':
                obj.sunday_12pm = True
            else:
                obj.sunday_12pm = False
            if request.POST.get('sunday_1pm') == 'on':
                obj.sunday_1pm = True
            else:
                obj.sunday_1pm = False
            if request.POST.get('sunday_2pm') == 'on':
                obj.sunday_2pm = True
            else:
                obj.sunday_2pm = False
            if request.POST.get('sunday_3pm') == 'on':
                obj.sunday_3pm = True
            else:
                obj.sunday_3pm = False
            if request.POST.get('sunday_4pm') == 'on':
                obj.sunday_4pm = True
            else:
                obj.sunday_4pm = False
            if request.POST.get('sunday_5pm') == 'on':
                obj.sunday_5pm = True
            else:
                obj.sunday_5pm = False
            if request.POST.get('sunday_6pm') == 'on':
                obj.sunday_6pm = True
            else:
                obj.sunday_6pm = False
            if request.POST.get('sunday_7pm') == 'on':
                obj.sunday_7pm = True
            else:
                obj.sunday_7pm = False
            if request.POST.get('sunday_8pm') == 'on':
                obj.sunday_8pm = True
            else:
                obj.sunday_8pm = False
            if request.POST.get('sunday_9pm') == 'on':
                obj.sunday_9pm = True
            else:
                obj.sunday_9pm = False
            if request.POST.get('sunday_10pm') == 'on':
                obj.sunday_10pm = True
            else:
                obj.sunday_10pm = False

            obj.sunday_recurrence =  request.POST.get('sunday_recurrence')
            obj.created_by = requesting_user
            obj.notes = request.POST.get('notes')

            obj.save()

            email_to_list = ['studio239@paintingwithatwist.com']
            string = 'https://admin.funartstudios.com/schedule/staff/review/' + str(obj.id)
            send_mail(
                'FAS Schedule Availability Change Request: ' + obj.user.first_name + ' ' + obj.user.last_name,
                string,
                'studio239@paintingwithatwist.com',
                email_to_list,
                fail_silently=False,
            )
            
        else:
            print('existing request')
            message = 'Your existing request has been re-submitted'

            obj = ScheduleChange.objects.get(user=requesting_user)

            obj.start_date = request.POST.get('start_date')

            if request.POST.get('monday_8am') == 'on':
                obj.monday_8am = True
            else:
                obj.monday_8am = False
            if request.POST.get('monday_9am') == 'on':
                obj.monday_9am = True
            else:
                obj.monday_9am = False
            if request.POST.get('monday_10am') == 'on':
                obj.monday_10am = True
            else:
                obj.monday_10am = False
            if request.POST.get('monday_11am') == 'on':
                obj.monday_11am = True
            else:
                obj.monday_11am = False
            if request.POST.get('monday_12pm') == 'on':
                obj.monday_12pm = True
            else:
                obj.monday_12pm = False
            if request.POST.get('monday_1pm') == 'on':
                obj.monday_1pm = True
            else:
                obj.monday_1pm = False
            if request.POST.get('monday_2pm') == 'on':
                obj.monday_2pm = True
            else:
                obj.monday_2pm = False
            if request.POST.get('monday_3pm') == 'on':
                obj.monday_3pm = True
            else:
                obj.monday_3pm = False
            if request.POST.get('monday_4pm') == 'on':
                obj.monday_4pm = True
            else:
                obj.monday_4pm = False
            if request.POST.get('monday_5pm') == 'on':
                obj.monday_5pm = True
            else:
                obj.monday_5pm = False
            if request.POST.get('monday_6pm') == 'on':
                obj.monday_6pm = True
            else:
                obj.monday_6pm = False
            if request.POST.get('monday_7pm') == 'on':
                obj.monday_7pm = True
            else:
                obj.monday_7pm = False
            if request.POST.get('monday_8pm') == 'on':
                obj.monday_8pm = True
            else:
                obj.monday_8pm = False
            if request.POST.get('monday_9pm') == 'on':
                obj.monday_9pm = True
            else:
                obj.monday_9pm = False
            if request.POST.get('monday_10pm') == 'on':
                obj.monday_10pm = True
            else:
                obj.monday_10pm = False

            obj.monday_recurrence =  request.POST.get('monday_recurrence')


            if request.POST.get('tuesday_8am') == 'on':
                obj.tuesday_8am = True
            else:
                obj.tuesday_8am = False
            if request.POST.get('tuesday_9am') == 'on':
                obj.tuesday_9am = True
            else:
                obj.tuesday_9am = False
            if request.POST.get('tuesday_10am') == 'on':
                obj.tuesday_10am = True
            else:
                obj.tuesday_10am = False
            if request.POST.get('tuesday_11am') == 'on':
                obj.tuesday_11am = True
            else:
                obj.tuesday_11am = False
            if request.POST.get('tuesday_12pm') == 'on':
                obj.tuesday_12pm = True
            else:
                obj.tuesday_12pm = False
            if request.POST.get('tuesday_1pm') == 'on':
                obj.tuesday_1pm = True
            else:
                obj.tuesday_1pm = False
            if request.POST.get('tuesday_2pm') == 'on':
                obj.tuesday_2pm = True
            else:
                obj.tuesday_2pm = False
            if request.POST.get('tuesday_3pm') == 'on':
                obj.tuesday_3pm = True
            else:
                obj.tuesday_3pm = False
            if request.POST.get('tuesday_4pm') == 'on':
                obj.tuesday_4pm = True
            else:
                obj.tuesday_4pm = False
            if request.POST.get('tuesday_5pm') == 'on':
                obj.tuesday_5pm = True
            else:
                obj.tuesday_5pm = False
            if request.POST.get('tuesday_6pm') == 'on':
                obj.tuesday_6pm = True
            else:
                obj.tuesday_6pm = False
            if request.POST.get('tuesday_7pm') == 'on':
                obj.tuesday_7pm = True
            else:
                obj.tuesday_7pm = False
            if request.POST.get('tuesday_8pm') == 'on':
                obj.tuesday_8pm = True
            else:
                obj.tuesday_8pm = False
            if request.POST.get('tuesday_9pm') == 'on':
                obj.tuesday_9pm = True
            else:
                obj.tuesday_9pm = False
            if request.POST.get('tuesday_10pm') == 'on':
                obj.tuesday_10pm = True
            else:
                obj.tuesday_10pm = False

            obj.tuesday_recurrence =  request.POST.get('tuesday_recurrence')


            if request.POST.get('wednesday_8am') == 'on':
                obj.wednesday_8am = True
            else:
                obj.wednesday_8am = False
            if request.POST.get('wednesday_9am') == 'on':
                obj.wednesday_9am = True
            else:
                obj.wednesday_9am = False
            if request.POST.get('wednesday_10am') == 'on':
                obj.wednesday_10am = True
            else:
                obj.wednesday_10am = False
            if request.POST.get('wednesday_11am') == 'on':
                obj.wednesday_11am = True
            else:
                obj.wednesday_11am = False
            if request.POST.get('wednesday_12pm') == 'on':
                obj.wednesday_12pm = True
            else:
                obj.wednesday_12pm = False
            if request.POST.get('wednesday_1pm') == 'on':
                obj.wednesday_1pm = True
            else:
                obj.wednesday_1pm = False
            if request.POST.get('wednesday_2pm') == 'on':
                obj.wednesday_2pm = True
            else:
                obj.wednesday_2pm = False
            if request.POST.get('wednesday_3pm') == 'on':
                obj.wednesday_3pm = True
            else:
                obj.wednesday_3pm = False
            if request.POST.get('wednesday_4pm') == 'on':
                obj.wednesday_4pm = True
            else:
                obj.wednesday_4pm = False
            if request.POST.get('wednesday_5pm') == 'on':
                obj.wednesday_5pm = True
            else:
                obj.wednesday_5pm = False
            if request.POST.get('wednesday_6pm') == 'on':
                obj.wednesday_6pm = True
            else:
                obj.wednesday_6pm = False
            if request.POST.get('wednesday_7pm') == 'on':
                obj.wednesday_7pm = True
            else:
                obj.wednesday_7pm = False
            if request.POST.get('wednesday_8pm') == 'on':
                obj.wednesday_8pm = True
            else:
                obj.wednesday_8pm = False
            if request.POST.get('wednesday_9pm') == 'on':
                obj.wednesday_9pm = True
            else:
                obj.wednesday_9pm = False
            if request.POST.get('wednesday_10pm') == 'on':
                obj.wednesday_10pm = True
            else:
                obj.wednesday_10pm = False

            obj.wednesday_recurrence =  request.POST.get('wednesday_recurrence')


            if request.POST.get('thursday_8am') == 'on':
                obj.thursday_8am = True
            else:
                obj.thursday_8am = False
            if request.POST.get('thursday_9am') == 'on':
                obj.thursday_9am = True
            else:
                obj.thursday_9am = False
            if request.POST.get('thursday_10am') == 'on':
                obj.thursday_10am = True
            else:
                obj.thursday_10am = False
            if request.POST.get('thursday_11am') == 'on':
                obj.thursday_11am = True
            else:
                obj.thursday_11am = False
            if request.POST.get('thursday_12pm') == 'on':
                obj.thursday_12pm = True
            else:
                obj.thursday_12pm = False
            if request.POST.get('thursday_1pm') == 'on':
                obj.thursday_1pm = True
            else:
                obj.thursday_1pm = False
            if request.POST.get('thursday_2pm') == 'on':
                obj.thursday_2pm = True
            else:
                obj.thursday_2pm = False
            if request.POST.get('thursday_3pm') == 'on':
                obj.thursday_3pm = True
            else:
                obj.thursday_3pm = False
            if request.POST.get('thursday_4pm') == 'on':
                obj.thursday_4pm = True
            else:
                obj.thursday_4pm = False
            if request.POST.get('thursday_5pm') == 'on':
                obj.thursday_5pm = True
            else:
                obj.thursday_5pm = False
            if request.POST.get('thursday_6pm') == 'on':
                obj.thursday_6pm = True
            else:
                obj.thursday_6pm = False
            if request.POST.get('thursday_7pm') == 'on':
                obj.thursday_7pm = True
            else:
                obj.thursday_7pm = False
            if request.POST.get('thursday_8pm') == 'on':
                obj.thursday_8pm = True
            else:
                obj.thursday_8pm = False
            if request.POST.get('thursday_9pm') == 'on':
                obj.thursday_9pm = True
            else:
                obj.thursday_9pm = False
            if request.POST.get('thursday_10pm') == 'on':
                obj.thursday_10pm = True
            else:
                obj.thursday_10pm = False

            obj.thursday_recurrence =  request.POST.get('thursday_recurrence')


            if request.POST.get('friday_8am') == 'on':
                obj.friday_8am = True
            else:
                obj.friday_8am = False
            if request.POST.get('friday_9am') == 'on':
                obj.friday_9am = True
            else:
                obj.friday_9am = False
            if request.POST.get('friday_10am') == 'on':
                obj.friday_10am = True
            else:
                obj.friday_10am = False
            if request.POST.get('friday_11am') == 'on':
                obj.friday_11am = True
            else:
                obj.friday_11am = False
            if request.POST.get('friday_12pm') == 'on':
                obj.friday_12pm = True
            else:
                obj.friday_12pm = False
            if request.POST.get('friday_1pm') == 'on':
                obj.friday_1pm = True
            else:
                obj.friday_1pm = False
            if request.POST.get('friday_2pm') == 'on':
                obj.friday_2pm = True
            else:
                obj.friday_2pm = False
            if request.POST.get('friday_3pm') == 'on':
                obj.friday_3pm = True
            else:
                obj.friday_3pm = False
            if request.POST.get('friday_4pm') == 'on':
                obj.friday_4pm = True
            else:
                obj.friday_4pm = False
            if request.POST.get('friday_5pm') == 'on':
                obj.friday_5pm = True
            else:
                obj.friday_5pm = False
            if request.POST.get('friday_6pm') == 'on':
                obj.friday_6pm = True
            else:
                obj.friday_6pm = False
            if request.POST.get('friday_7pm') == 'on':
                obj.friday_7pm = True
            else:
                obj.friday_7pm = False
            if request.POST.get('friday_8pm') == 'on':
                obj.friday_8pm = True
            else:
                obj.friday_8pm = False
            if request.POST.get('friday_9pm') == 'on':
                obj.friday_9pm = True
            else:
                obj.friday_9pm = False
            if request.POST.get('friday_10pm') == 'on':
                obj.friday_10pm = True
            else:
                obj.friday_10pm = False

            obj.friday_recurrence =  request.POST.get('friday_recurrence')


            if request.POST.get('saturday_8am') == 'on':
                obj.saturday_8am = True
            else:
                obj.saturday_8am = False
            if request.POST.get('saturday_9am') == 'on':
                obj.saturday_9am = True
            else:
                obj.saturday_9am = False
            if request.POST.get('saturday_10am') == 'on':
                obj.saturday_10am = True
            else:
                obj.saturday_10am = False
            if request.POST.get('saturday_11am') == 'on':
                obj.saturday_11am = True
            else:
                obj.saturday_11am = False
            if request.POST.get('saturday_12pm') == 'on':
                obj.saturday_12pm = True
            else:
                obj.saturday_12pm = False
            if request.POST.get('saturday_1pm') == 'on':
                obj.saturday_1pm = True
            else:
                obj.saturday_1pm = False
            if request.POST.get('saturday_2pm') == 'on':
                obj.saturday_2pm = True
            else:
                obj.saturday_2pm = False
            if request.POST.get('saturday_3pm') == 'on':
                obj.saturday_3pm = True
            else:
                obj.saturday_3pm = False
            if request.POST.get('saturday_4pm') == 'on':
                obj.saturday_4pm = True
            else:
                obj.saturday_4pm = False
            if request.POST.get('saturday_5pm') == 'on':
                obj.saturday_5pm = True
            else:
                obj.saturday_5pm = False
            if request.POST.get('saturday_6pm') == 'on':
                obj.saturday_6pm = True
            else:
                obj.saturday_6pm = False
            if request.POST.get('saturday_7pm') == 'on':
                obj.saturday_7pm = True
            else:
                obj.saturday_7pm = False
            if request.POST.get('saturday_8pm') == 'on':
                obj.saturday_8pm = True
            else:
                obj.saturday_8pm = False
            if request.POST.get('saturday_9pm') == 'on':
                obj.saturday_9pm = True
            else:
                obj.saturday_9pm = False
            if request.POST.get('saturday_10pm') == 'on':
                obj.saturday_10pm = True
            else:
                obj.saturday_10pm = False

            obj.saturday_recurrence =  request.POST.get('saturday_recurrence')


            if request.POST.get('sunday_8am') == 'on':
                obj.sunday_8am = True
            else:
                obj.sunday_8am = False
            if request.POST.get('sunday_9am') == 'on':
                obj.sunday_9am = True
            else:
                obj.sunday_9am = False
            if request.POST.get('sunday_10am') == 'on':
                obj.sunday_10am = True
            else:
                obj.sunday_10am = False
            if request.POST.get('sunday_11am') == 'on':
                obj.sunday_11am = True
            else:
                obj.sunday_11am = False
            if request.POST.get('sunday_12pm') == 'on':
                obj.sunday_12pm = True
            else:
                obj.sunday_12pm = False
            if request.POST.get('sunday_1pm') == 'on':
                obj.sunday_1pm = True
            else:
                obj.sunday_1pm = False
            if request.POST.get('sunday_2pm') == 'on':
                obj.sunday_2pm = True
            else:
                obj.sunday_2pm = False
            if request.POST.get('sunday_3pm') == 'on':
                obj.sunday_3pm = True
            else:
                obj.sunday_3pm = False
            if request.POST.get('sunday_4pm') == 'on':
                obj.sunday_4pm = True
            else:
                obj.sunday_4pm = False
            if request.POST.get('sunday_5pm') == 'on':
                obj.sunday_5pm = True
            else:
                obj.sunday_5pm = False
            if request.POST.get('sunday_6pm') == 'on':
                obj.sunday_6pm = True
            else:
                obj.sunday_6pm = False
            if request.POST.get('sunday_7pm') == 'on':
                obj.sunday_7pm = True
            else:
                obj.sunday_7pm = False
            if request.POST.get('sunday_8pm') == 'on':
                obj.sunday_8pm = True
            else:
                obj.sunday_8pm = False
            if request.POST.get('sunday_9pm') == 'on':
                obj.sunday_9pm = True
            else:
                obj.sunday_9pm = False
            if request.POST.get('sunday_10pm') == 'on':
                obj.sunday_10pm = True
            else:
                obj.sunday_10pm = False

            obj.sunday_recurrence =  request.POST.get('sunday_recurrence')
            obj.created_by = requesting_user
            obj.notes = request.POST.get('notes')

            obj.save()

            email_to_list = ['studio239@paintingwithatwist.com']
            string = 'https://admin.funartstudios.com/schedule/staff/review/' + str(obj.id)
            send_mail(
                'FAS Schedule Availability Change Request: ' + obj.user.first_name + ' ' + obj.user.last_name,
                string,
                'studio239@paintingwithatwist.com',
                email_to_list,
                fail_silently=False,
            )



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
            "message": message,
            "schedule_count": schedule_count,
        }
        return render(request, "schedule/list.html", context)

    else:

        try:
            qs = ScheduleChange.objects.get(active=True, user=requesting_user)
            if qs:
                status = qs.status
        except:
            qs = Typical.objects.get(active=True, user=requesting_user)
            status = None

        howmany = None
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 20)
        # schedule_count = paginator.count
        # try:
        #     schedules = paginator.page(page)
        # except PageNotAnInteger:
        #     schedules = paginator.page(1)
        # except EmptyPage:
        #     schedules = paginator.page(paginator.num_pages)

        context = {
            # "schedules": schedules,
            "x": qs,
            "status": status,
            "howmany": howmany,
            # "schedule_count": schedule_count,
        }

        return render(request, "schedule/staff-edit-list.html", context)


@permission_required('schedule.add_typical')
def schedule_mgmt_review_view(request, id=None):
    qs_new = ScheduleChange.objects.get(active=True, id=id)
    qs_orig = Typical.objects.get(user=qs_new.user)
    status = qs_new.get_status_display
    howmany = None

    context = {
        "x": qs_new,
        "y": qs_orig,
        "howmany": howmany,
        "status": status,
    }
    return render(request, "schedule/mgmt-review.html", context)

@permission_required('schedule.add_typical')
def schedule_mgmt_approve_view(request, id=None):
    qs_new = ScheduleChange.objects.get(active=True, id=id)
    obj = Typical.objects.get(user=qs_new.user)
    status = qs_new.get_status_display
    howmany = None
    print(qs_new)
    obj.start_date = qs_new.start_date

    obj.monday_8am = qs_new.monday_8am
    obj.monday_9am = qs_new.monday_9am
    obj.monday_10am = qs_new.monday_10am
    obj.monday_11am = qs_new.monday_11am
    obj.monday_12pm = qs_new.monday_12pm
    obj.monday_1pm = qs_new.monday_1pm
    obj.monday_2pm = qs_new.monday_2pm
    obj.monday_3pm = qs_new.monday_3pm
    obj.monday_4pm = qs_new.monday_4pm
    obj.monday_5pm = qs_new.monday_5pm
    obj.monday_6pm = qs_new.monday_6pm
    obj.monday_7pm = qs_new.monday_7pm
    obj.monday_8pm = qs_new.monday_8pm
    obj.monday_9pm = qs_new.monday_9pm
    obj.monday_10pm = qs_new.monday_10pm
    obj.monday_recurrence =  qs_new.monday_recurrence

    obj.tuesday_8am = qs_new.tuesday_8am
    obj.tuesday_9am = qs_new.tuesday_9am
    obj.tuesday_10am = qs_new.tuesday_10am
    obj.tuesday_11am = qs_new.tuesday_11am
    obj.tuesday_12pm = qs_new.tuesday_12pm
    obj.tuesday_1pm = qs_new.tuesday_1pm
    obj.tuesday_2pm = qs_new.tuesday_2pm
    obj.tuesday_3pm = qs_new.tuesday_3pm
    obj.tuesday_4pm = qs_new.tuesday_4pm
    obj.tuesday_5pm = qs_new.tuesday_5pm
    obj.tuesday_6pm = qs_new.tuesday_6pm
    obj.tuesday_7pm = qs_new.tuesday_7pm
    obj.tuesday_8pm = qs_new.tuesday_8pm
    obj.tuesday_9pm = qs_new.tuesday_9pm
    obj.tuesday_10pm = qs_new.tuesday_10pm
    obj.tuesday_recurrence =  qs_new.tuesday_recurrence

    obj.wednesday_8am = qs_new.wednesday_8am
    obj.wednesday_9am = qs_new.wednesday_9am
    obj.wednesday_10am = qs_new.wednesday_10am
    obj.wednesday_11am = qs_new.wednesday_11am
    obj.wednesday_12pm = qs_new.wednesday_12pm
    obj.wednesday_1pm = qs_new.wednesday_1pm
    obj.wednesday_2pm = qs_new.wednesday_2pm
    obj.wednesday_3pm = qs_new.wednesday_3pm
    obj.wednesday_4pm = qs_new.wednesday_4pm
    obj.wednesday_5pm = qs_new.wednesday_5pm
    obj.wednesday_6pm = qs_new.wednesday_6pm
    obj.wednesday_7pm = qs_new.wednesday_7pm
    obj.wednesday_8pm = qs_new.wednesday_8pm
    obj.wednesday_9pm = qs_new.wednesday_9pm
    obj.wednesday_10pm = qs_new.wednesday_10pm
    obj.wednesday_recurrence =  qs_new.wednesday_recurrence

    obj.thursday_8am = qs_new.thursday_8am
    obj.thursday_9am = qs_new.thursday_9am
    obj.thursday_10am = qs_new.thursday_10am
    obj.thursday_11am = qs_new.thursday_11am
    obj.thursday_12pm = qs_new.thursday_12pm
    obj.thursday_1pm = qs_new.thursday_1pm
    obj.thursday_2pm = qs_new.thursday_2pm
    obj.thursday_3pm = qs_new.thursday_3pm
    obj.thursday_4pm = qs_new.thursday_4pm
    obj.thursday_5pm = qs_new.thursday_5pm
    obj.thursday_6pm = qs_new.thursday_6pm
    obj.thursday_7pm = qs_new.thursday_7pm
    obj.thursday_8pm = qs_new.thursday_8pm
    obj.thursday_9pm = qs_new.thursday_9pm
    obj.thursday_10pm = qs_new.thursday_10pm
    obj.thursday_recurrence =  qs_new.thursday_recurrence

    obj.friday_8am = qs_new.friday_8am
    obj.friday_9am = qs_new.friday_9am
    obj.friday_10am = qs_new.friday_10am
    obj.friday_11am = qs_new.friday_11am
    obj.friday_12pm = qs_new.friday_12pm
    obj.friday_1pm = qs_new.friday_1pm
    obj.friday_2pm = qs_new.friday_2pm
    obj.friday_3pm = qs_new.friday_3pm
    obj.friday_4pm = qs_new.friday_4pm
    obj.friday_5pm = qs_new.friday_5pm
    obj.friday_6pm = qs_new.friday_6pm
    obj.friday_7pm = qs_new.friday_7pm
    obj.friday_8pm = qs_new.friday_8pm
    obj.friday_9pm = qs_new.friday_9pm
    obj.friday_10pm = qs_new.friday_10pm
    obj.friday_recurrence =  qs_new.friday_recurrence

    obj.saturday_8am = qs_new.saturday_8am
    obj.saturday_9am = qs_new.saturday_9am
    obj.saturday_10am = qs_new.saturday_10am
    obj.saturday_11am = qs_new.saturday_11am
    obj.saturday_12pm = qs_new.saturday_12pm
    obj.saturday_1pm = qs_new.saturday_1pm
    obj.saturday_2pm = qs_new.saturday_2pm
    obj.saturday_3pm = qs_new.saturday_3pm
    obj.saturday_4pm = qs_new.saturday_4pm
    obj.saturday_5pm = qs_new.saturday_5pm
    obj.saturday_6pm = qs_new.saturday_6pm
    obj.saturday_7pm = qs_new.saturday_7pm
    obj.saturday_8pm = qs_new.saturday_8pm
    obj.saturday_9pm = qs_new.saturday_9pm
    obj.saturday_10pm = qs_new.saturday_10pm
    obj.saturday_recurrence =  qs_new.saturday_recurrence

    obj.sunday_8am = qs_new.sunday_8am
    obj.sunday_9am = qs_new.sunday_9am
    obj.sunday_10am = qs_new.sunday_10am
    obj.sunday_11am = qs_new.sunday_11am
    obj.sunday_12pm = qs_new.sunday_12pm
    obj.sunday_1pm = qs_new.sunday_1pm
    obj.sunday_2pm = qs_new.sunday_2pm
    obj.sunday_3pm = qs_new.sunday_3pm
    obj.sunday_4pm = qs_new.sunday_4pm
    obj.sunday_5pm = qs_new.sunday_5pm
    obj.sunday_6pm = qs_new.sunday_6pm
    obj.sunday_7pm = qs_new.sunday_7pm
    obj.sunday_8pm = qs_new.sunday_8pm
    obj.sunday_9pm = qs_new.sunday_9pm
    obj.sunday_10pm = qs_new.sunday_10pm
    obj.sunday_recurrence =  qs_new.sunday_recurrence
    obj.updated_by = request.user
    obj.notes = qs_new.notes

    obj.save()

    qs_new.status = 'c'
    qs_new.active = False
    qs_new.delete()

    return redirect('schedule:list')


@permission_required('schedule.view_timeoffrequest')
def schedule_staff_timeoff_detail_view(request, id=None):
    hx_url = reverse("schedule:hx-timeoffdetail", kwargs={"id": id})
    timeoff_obj = TimeOffRequest.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "event_obj": timeoff_obj
    }
    return render(request, "schedule/timeoffrequest.html", context)


@permission_required('schedule.view_timeoffrequest')
def hx_schedule_staff_timeoff_detail_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = TimeOffRequest.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
    }
    return render(request, "schedule/partials/timeoffdetail.html", context)


@permission_required('schedule.change_typical')
def schedule_mgmt_timeoff_detail_view(request, id=None):
    hx_url = reverse("schedule:hx-mgmttimeoffdetail", kwargs={"id": id})
    timeoff_obj = TimeOffRequest.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "event_obj": timeoff_obj
    }
    return render(request, "schedule/timeoffrequest.html", context)

@permission_required('schedule.change_typical')
def hx_schedule_mgmt_timeoff_detail_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = TimeOffRequest.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
    }
    return render(request, "schedule/partials/timeoffdetail.html", context)

 
@permission_required('schedule.add_timeoffrequest')
def schedule_staff_create_timeoff_view(request):
    form = TimeOffForm(request.POST or None)
    today = datetime.date.today()
    existing = TimeOffRequest.objects.filter(active=True, user=request.user, end_date__gte=today).order_by('start_date')
    context = {
        "form": form,
        "existing": existing
    }
    if request.POST:
        try: 
            if form.is_valid():
                print('valid form submitted')
                obj = form.save(commit=False)
                obj.user = request.user
                obj.created_by = request.user
                obj.save()

                email_to_list = ['studio239@paintingwithatwist.com']
                string = 'https://admin.funartstudios.com/account/login/?next=/schedule/mgmt/timeoff/' + str(obj.id) + '\n' + 'Starting on: ' + str(obj.start_date) + ' through ' + str(obj.end_date) +  '. \n' + 'Note: ' + obj.notes
                send_mail(
                    'FAS Schedule Time Off Request: ' + obj.user.first_name + ' ' + obj.user.last_name,
                    string,
                    'studio239@paintingwithatwist.com',
                    email_to_list,
                    fail_silently=False,
                )
                if request.htmx:
                    headers = {
                        "HX-Redirect": obj.get_absolute_url()
                    }
                    return HttpResponse('Created', headers=headers)
                return redirect(obj.get_absolute_url())
        except IntegrityError:
            context['message'] = 'Failed to Save. Check fields and try again'
            return render(request, "schedule/partials/forms.html", context)

    else:
        return render(request, "schedule/create-update-timeoff.html", context) 



@permission_required('schedule.change_timeoffrequest')
def schedule_staff_update_view(request, id=None):
    obj = get_object_or_404(TimeOffRequest, id=id, user=request.user)
    form = TimeOffForm(request.POST or None, instance=obj)
    today = datetime.date.today()
    existing = TimeOffRequest.objects.filter(active=True, user=request.user, end_date__gte=today).exclude(id=id).order_by('start_date')

    context = {
        "form": form,
        "object": obj,
        "existing": existing
    }
    if form.is_valid():
        obj.updated_by = request.user
        obj.save()
        form.save()

        email_to_list = ['studio239@paintingwithatwist.com']
        string = 'https://admin.funartstudios.com/account/login/?next=/schedule/mgmt/timeoff/' + str(obj.id) + '\n' + 'Starting on: ' + str(obj.start_date) + ' through ' + str(obj.end_date) +  '. \n' + 'Note: ' + obj.notes
        send_mail(
            'Updated: FAS Schedule Time Off Request: ' + obj.user.first_name + ' ' + obj.user.last_name,
            string,
            'studio239@paintingwithatwist.com',
            email_to_list,
            fail_silently=False,
        )


        context['message'] = 'Time off request data saved.'
    if request.htmx:
        headers = {
            "HX-Redirect": '/schedule/staff'
        }
        return HttpResponse('Created', headers=headers)
        # return render(request, "schedule/partials/forms.html", context)
    return render(request, "schedule/create-update-timeoff.html", context) 



@permission_required('schedule.change_typical')
def schedule_mgmt_timeoff_approve_view(request, id=None):
    obj = get_object_or_404(TimeOffRequest, id=id)
    obj.status = 'c'
    obj.updated_by = request.user
    obj.save()

    context = {
        "object": obj,
    }
    email_to_list = [obj.user.email, 'studio239@paintingwithatwist.com']
    string = 'https://admin.funartstudios.com/account/login/?next=/schedule/staff/timeoff/' + str(obj.id) + '\n' + 'Starting on: ' + str(obj.start_date) + ' through ' + str(obj.end_date) +  '. \n' + 'Note: ' + obj.notes
    send_mail(
        'Approved: FAS Schedule Time Off Request: ' + obj.user.first_name + ' ' + obj.user.last_name,
        string,
        'studio239@paintingwithatwist.com',
        email_to_list,
        fail_silently=False,
    )

    context['message'] = 'Time off request approved.'

    return redirect('/schedule')



@permission_required('schedule.delete_timeoffrequest')
def schedule_staff_timeoff_delete_view(request, id=None):
    try:
        obj = TimeOffRequest.objects.get(id=id, user=request.user)
        obj.delete()
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    success_url = reverse('schedule:staff')
    return redirect('/schedule/staff')
    # context = {
    #     "object": obj
    # }
    # return render(request, "schedule/list.html", context)
