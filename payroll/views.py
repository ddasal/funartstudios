import decimal
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from events.models import Event, EventCustomer, EventStaff, EventTip
from products.models import Product, PurchaseItem, PurchaseOrder
from payroll.forms import ReportForm
from django.db.models import Q
# from .forms import EventForm, EventStaffForm, EventCustomerForm
from payroll.models import PayReport
from decimal import Decimal

# Create your views here.

@permission_required('payroll.view_report')
def report_list_view(request):
    qs = PayReport.objects.all().order_by('-start_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    report_count = paginator.count
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    context = {
        "reports": reports,
        "report_count": report_count
    }
    return render(request, "payroll/list.html", context)

@permission_required('payroll.view_report')
def report_detail_view(request, id=None):
    hx_url = reverse("payroll:hx-detail", kwargs={"id": id})
    report_obj = PayReport.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "report_obj": report_obj
    }
    return render(request, "payroll/detail.html", context)



@permission_required('payroll.delete_report')
def report_delete_view(request, id=None):
    try:
        obj = PayReport.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            parent_obj = obj
            events = Event.objects.filter(payroll_report=parent_obj)
            for each in events:
                each.payroll_report = None
                each.save()
            obj.delete()
            success_url = reverse('payroll:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)
        else:
            success_url = reverse('payroll:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url,
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "payroll/delete.html", context)


@permission_required('payroll.view_report')
def report_detail_hx_view(request, id=None):
    hx_url = reverse("payroll:hx-staff-summary", kwargs={"id": id})
    if not request.htmx:
        raise Http404
    try:
        obj = PayReport.objects.get(id=id)
        events = Event.objects.filter(date__range=(obj.start_date, obj.end_date)).order_by('date', 'time').annotate(worker_count=Count('eventstaff'))
        staff_count = EventStaff.objects.all().filter(event__payroll_report=obj).order_by('user').distinct('user').count()
        payroll_gross = 0
        events_without_workers = 0
        total_stage_hours = 0
        total_floor_hours = 0
        total_team_hours = 0
        total_total_hours = 0
        total_stage_hourly_pay = 0
        total_floor_hourly_pay = 0
        total_team_hourly_pay = 0
        total_total_hourly_pay = 0
        total_stage_tip_pay = 0
        total_floor_tip_pay = 0
        total_team_tip_pay = 0
        total_total_tip_pay = 0
        total_stage_commission_pay = 0
        total_floor_commission_pay = 0
        total_team_commission_pay = 0
        total_total_commission_pay = 0
        total_stage_pay = 0
        total_floor_pay = 0
        total_team_pay = 0
        total_total_pay = 0
        for event in events:
            event.payroll_report = obj
            event.save()
            if event.worker_count == 0:
                events_without_workers = events_without_workers + 1
            tip_details = EventTip.objects.all().filter(event=event.id)
            event.count_stage = EventStaff.objects.all().filter(event=event.id, role='s').count()
            event.count_other = EventStaff.objects.all().filter(Q(role='f') | Q(role='t'), event=event.id).count()
            total_stage_tips = 0
            total_floor_tips = 0 
            if tip_details:
                for tip in tip_details:
                    total_stage_tips = total_stage_tips + tip.stage_amount
                    total_floor_tips = total_floor_tips + tip.floor_amount
            event.total_stage_tips = total_stage_tips
            event.total_floor_tips = total_floor_tips
            event.total_total_tips = total_stage_tips + total_floor_tips
            if event.count_other == 0:
                if event.count_stage == 1:
                    update_tip_stage = EventStaff.objects.get(event=event.id, role='s')
                    total_stage_hours = total_stage_hours + update_tip_stage.hours
                    total_stage_hourly_pay = total_stage_hourly_pay + update_tip_stage.hourly_pay
                    update_tip_stage.tip_pay = event.total_total_tips
                    total_stage_tip_pay = total_stage_tip_pay + update_tip_stage.tip_pay
                    update_tip_stage.save()
                elif event.count_stage > 1:
                    tip_each = event.total_total_tips / event.count_stage
                    update_tip = EventStaff.objects.filter(event=event.id)
                    for staff in update_tip:
                        if staff.role == 's':
                            total_stage_hours = total_stage_hours + staff.hours
                            total_stage_hourly_pay = total_stage_hourly_pay + staff.hourly_pay
                            staff.tip_pay = tip_each
                            total_stage_tip_pay = total_stage_tip_pay + staff.tip_pay
                            staff.save()
                elif event.count_stage == 0:
                    total_stage_tip_pay = total_stage_tip_pay + event.total_total_tips
            if event.count_other > 0:
                if event.count_stage == 1:
                    update_tip_stage = EventStaff.objects.get(event=event.id, role='s')
                    total_stage_hours = total_stage_hours + update_tip_stage.hours
                    total_stage_hourly_pay = total_stage_hourly_pay + update_tip_stage.hourly_pay
                    update_tip_stage.tip_pay = event.total_stage_tips
                    total_stage_tip_pay = total_stage_tip_pay + update_tip_stage.tip_pay
                    update_tip_stage.save()
                elif event.count_stage > 1:
                    tip_each = event.total_stage_tips / event.count_stage
                    update_tip = EventStaff.objects.filter(event=event.id, role='s')
                    for staff in update_tip:
                        if staff.role == 's':
                            total_stage_hours = total_stage_hours + staff.hours
                            total_stage_hourly_pay = total_stage_hourly_pay + staff.hourly_pay
                            staff.tip_pay = tip_each
                            total_stage_tip_pay = total_stage_tip_pay + staff.tip_pay
                            staff.save()
                if event.count_other == 1:
                    update_tip = EventStaff.objects.get(Q(role='f') | Q(role='t'), event=event.id)
                    update_tip.tip_pay = event.total_floor_tips
                    if update_tip.role == 'f':
                        total_floor_hours = total_floor_hours + update_tip.hours
                        total_floor_hourly_pay = total_floor_hourly_pay + update_tip.hourly_pay
                        total_floor_tip_pay = total_floor_tip_pay + update_tip.tip_pay
                    elif update_tip.role == 't':
                        total_team_hours = total_team_hours + update_tip.hours
                        total_team_hourly_pay = total_team_hourly_pay + update_tip.hourly_pay
                        total_team_tip_pay = total_team_tip_pay + update_tip.tip_pay
                    update_tip.save()
                elif event.count_other > 1:
                    tip_each = event.total_floor_tips / event.count_other
                    update_tip = EventStaff.objects.filter(Q(role='f') | Q(role='t'), event=event.id)
                    for staff in update_tip:
                        if staff.role == 'f':
                            total_floor_hours = total_floor_hours + staff.hours
                            total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                        elif staff.role == 't':
                            total_team_hours = total_team_hours + staff.hours
                            total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                        staff.tip_pay = tip_each
                        staff.save()
            try:
                kit_sales = EventCustomer.objects.filter(event=event.id, type='h')
                if kit_sales:
                    kit_count = 0
                    for kit in kit_sales:
                        kit_count = kit_count + kit.quantity
                    if kit_count > 0:
                        event.count_staff = int(event.count_other) + int(event.count_stage)
                        update_commission = EventStaff.objects.filter(event=event.id)
                        if event.count_staff == 1:
                            for staff in update_commission:
                                staff.commission_pay = Decimal(5.00) * kit_count
                                staff.save()
                                if staff.role == 's':
                                    total_stage_commission_pay = total_stage_commission_pay + staff.commission_pay
                                elif staff.role == 'f':
                                    total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                                elif staff.role == 't':
                                    total_team_commission_pay = total_team_commission_pay + staff.commission_pay
                        if event.count_staff == 2:
                            for staff in update_commission:
                                staff.commission_pay = Decimal(3.00) * kit_count
                                staff.save()                        
                                if staff.role == 's':
                                    total_stage_commission_pay = total_stage_commission_pay + staff.commission_pay
                                elif staff.role == 'f':
                                    total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                                elif staff.role == 't':
                                    total_team_commission_pay = total_team_commission_pay + staff.commission_pay
                        if event.count_staff > 2:
                            for staff in update_commission:
                                staff.commission_pay = Decimal(2.00) * kit_count
                                staff.save()     
                                if staff.role == 's':
                                    total_stage_commission_pay = total_stage_commission_pay + staff.commission_pay
                                elif staff.role == 'f':
                                    total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                                elif staff.role == 't':
                                    total_team_commission_pay = total_team_commission_pay + staff.commission_pay
            except:
                kit_count is None
        total_total_hours = total_stage_hours + total_floor_hours + total_team_hours
        total_total_hourly_pay = total_stage_hourly_pay + total_floor_hourly_pay + total_team_hourly_pay
        total_total_tip_pay = total_stage_tip_pay + total_floor_tip_pay + total_team_tip_pay
        total_total_commission_pay = total_stage_commission_pay + total_floor_commission_pay + total_team_commission_pay
        total_stage_pay = total_stage_hourly_pay + total_stage_tip_pay + total_stage_commission_pay
        total_floor_pay = total_floor_hourly_pay + total_floor_tip_pay + total_floor_commission_pay
        total_team_pay = total_team_hourly_pay + total_team_tip_pay + total_team_commission_pay
        total_total_pay = total_stage_pay + total_floor_pay + total_team_pay
        obj.staff_count = staff_count
        obj.payroll_gross = total_total_pay
        obj.save()

 
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "events": events,
        "hx_url": hx_url,
        "payroll_gross": payroll_gross,
        "events_without_workers": events_without_workers,
        "total_stage_hours": total_stage_hours,
        "total_floor_hours": total_floor_hours,
        "total_team_hours": total_team_hours,
        "total_total_hours": total_total_hours,
        "total_stage_hourly_pay": total_stage_hourly_pay,
        "total_floor_hourly_pay": total_floor_hourly_pay,
        "total_team_hourly_pay": total_team_hourly_pay,
        "total_total_hourly_pay": total_total_hourly_pay,
        "total_stage_tip_pay": total_stage_tip_pay,
        "total_floor_tip_pay": total_floor_tip_pay,
        "total_team_tip_pay": total_team_tip_pay,
        "total_total_tip_pay": total_total_tip_pay,
        "total_stage_commission_pay": total_stage_commission_pay,
        "total_floor_commission_pay": total_floor_commission_pay,
        "total_team_commission_pay": total_team_commission_pay,
        "total_total_commission_pay": total_total_commission_pay,
        "total_stage_pay": total_stage_pay,
        "total_floor_pay": total_floor_pay,
        "total_team_pay": total_team_pay,
        "total_total_pay": total_total_pay
    }
    return render(request, "payroll/partials/detail.html", context)
 


@permission_required('payroll.add_report')
def report_create_view(request):
    form = ReportForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse('Created', headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "payroll/create-update.html", context) 

@permission_required('payroll.change_report')
def report_update_view(request, id=None):
    obj = get_object_or_404(PayReport, id=id)
    form = ReportForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Report data saved.'
    if request.htmx:
        return render(request, "payroll/partials/forms.html", context)
    return render(request, "payroll/create-update.html", context) 


@permission_required('payroll.change_report')
def report_hx_mark_complete(request, id=None):
    # if not request.htmx:
    #     raise Http404
    try:
        parent_obj = PayReport.objects.get(id=id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not found.")
    else:
        children = Event.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for event in children:
            event.payroll_status = 'c'
            event.save()
            staff = EventStaff.objects.filter(event=event.id)
            tips = EventTip.objects.filter(event=event.id)
            for each in staff:
                each.status = 'c'
                each.save()
            for each in tips:
                each.status = 'c'
                each.save()
        parent_obj.status = 'c'
        parent_obj.save()

        success_url = reverse('payroll:list')
        # if request.htmx:
        #     headers = {
        #         "HX-Redirect": success_url
        #     }
        #     return HttpResponse('Success', headers=headers)
        return redirect(success_url)


@permission_required('payroll.change_report')
def report_hx_mark_pending(request, id=None):
    # if not request.htmx:
    #     raise Http404
    try:
        parent_obj = PayReport.objects.get(id=id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not found.")
    else:
        parent_obj.status = 'p'
        parent_obj.save()
        children = Event.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for event in children:
            event.payroll_status = 'p'
            event.save()
            staff = EventStaff.objects.filter(event=event.id)
            tips = EventTip.objects.filter(event=event.id)
            for each in staff:
                each.status = 'p'
                each.save()
            for each in tips:
                each.status = 'p'
                each.save()
        success_url = reverse('payroll:list')
        # if request.htmx:
        #     headers = {
        #         "HX-Redirect": success_url
        #     }
        #     return HttpResponse('Success', headers=headers)
        return redirect(success_url)


@login_required
def report_staff_detail_view(request, id=None):
    user = request.user
    hx_url = reverse("payroll:hx-staff-detail", kwargs={"id": id})
    report_obj = PayReport.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "report_obj": report_obj
    }
    return render(request, "payroll/staff-detail.html", context)


@login_required
def report_staff_detail_hx_view(request, id=None, user=None):
    if not request.htmx:
        raise Http404
    try:
        obj = PayReport.objects.get(id=id)
        events = Event.objects.all().filter(payroll_report=obj).order_by('date', 'time')
        event_staff = EventStaff.objects.all().filter(event__payroll_report=obj, user=request.user.id)
        total_stage_hours = 0
        total_floor_hours = 0
        total_team_hours = 0
        total_total_hours = 0
        total_stage_hourly_pay = 0
        total_floor_hourly_pay = 0
        total_team_hourly_pay = 0
        total_total_hourly_pay = 0
        total_stage_tip_pay = 0
        total_floor_tip_pay = 0
        total_team_tip_pay = 0
        total_total_tip_pay = 0
        total_stage_commission_pay = 0
        total_floor_commission_pay = 0
        total_team_commission_pay = 0
        total_total_commission_pay = 0
        total_stage_pay = 0
        total_floor_pay = 0
        total_team_pay = 0
        total_total_pay = 0
        for staff in event_staff:
            if staff.role == 's':
                total_stage_hours = total_stage_hours + staff.hours
                total_stage_hourly_pay = total_stage_hourly_pay + staff.hourly_pay
                total_stage_tip_pay = total_stage_tip_pay + staff.tip_pay
                total_stage_commission_pay = total_stage_commission_pay + staff.commission_pay
                total_stage_pay = total_stage_pay + total_stage_hourly_pay + total_stage_commission_pay + total_stage_tip_pay
            elif staff.role == 'f':
                total_floor_hours = total_floor_hours + staff.hours
                total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                total_floor_tip_pay = total_floor_tip_pay + staff.tip_pay
                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                total_floor_pay = total_floor_pay + total_floor_hourly_pay + total_floor_commission_pay + total_floor_tip_pay
            elif staff.role == 't':
                total_team_hours = total_team_hours + staff.hours
                total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                total_team_tip_pay = total_team_tip_pay + staff.tip_pay
                total_team_commission_pay = total_team_commission_pay + staff.commission_pay
                total_team_pay = total_team_pay + total_team_hourly_pay + total_team_commission_pay + total_team_tip_pay
        total_total_hours = total_stage_hours + total_floor_hours + total_team_hours
        total_total_hourly_pay = total_stage_hourly_pay + total_floor_hourly_pay + total_team_hourly_pay
        total_total_tip_pay = total_stage_tip_pay + total_floor_tip_pay + total_team_tip_pay
        total_total_commission_pay = total_stage_commission_pay + total_floor_commission_pay + total_team_commission_pay
        total_total_pay = total_stage_pay + total_floor_pay + total_team_pay

    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "event_staff": event_staff,
        "total_stage_hours": total_stage_hours,
        "total_floor_hours": total_floor_hours,
        "total_team_hours": total_team_hours,
        "total_total_hours": total_total_hours,
        "total_stage_hourly_pay": total_stage_hourly_pay,
        "total_floor_hourly_pay": total_floor_hourly_pay,
        "total_team_hourly_pay": total_team_hourly_pay,
        "total_total_hourly_pay": total_total_hourly_pay,
        "total_stage_tip_pay": total_stage_tip_pay,
        "total_floor_tip_pay": total_floor_tip_pay,
        "total_team_tip_pay": total_team_tip_pay,
        "total_total_tip_pay": total_total_tip_pay,
        "total_stage_commission_pay": total_stage_commission_pay,
        "total_floor_commission_pay": total_floor_commission_pay,
        "total_team_commission_pay": total_team_commission_pay,
        "total_total_commission_pay": total_total_commission_pay,
        "total_stage_pay": total_stage_pay,
        "total_floor_pay": total_floor_pay,
        "total_team_pay": total_team_pay,
        "total_total_pay": total_total_pay
    }
    return render(request, "payroll/partials/staff-detail.html", context)
 

@login_required
def report_staff_list_view(request):
    qs = PayReport.objects.filter(event__eventstaff__user=request.user.id).order_by('-start_date').distinct()
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    report_count = paginator.count
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    context = {
        "reports": reports,
        "report_count": report_count
    }
    return render(request, "payroll/staff-list.html", context)


@permission_required('payroll.change_report')
def report_staff_summary_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = PayReport.objects.get(id=id)
        eventstaff_list = EventStaff.objects.filter(event__payroll_report=obj)
        distinct_users = eventstaff_list.values('user').distinct() #.exclude(Q(user=7) | Q(user=1))
        for staff in distinct_users:
            staff['total_stage_hours'] = 0
            staff['total_floor_hours'] = 0
            staff['total_team_hours'] = 0
            staff['total_total_hours'] = 0
            staff['total_stage_hourly_pay'] = 0
            staff['total_floor_hourly_pay'] = 0
            staff['total_team_hourly_pay'] = 0
            staff['total_total_hourly_pay'] = 0
            staff['total_stage_tip_pay'] = 0
            staff['total_floor_tip_pay'] = 0
            staff['total_team_tip_pay'] = 0
            staff['total_total_tip_pay'] = 0
            staff['total_stage_commission_pay'] = 0
            staff['total_floor_commission_pay'] = 0
            staff['total_team_commission_pay'] = 0
            staff['total_total_commission_pay'] = 0
            staff['total_stage_pay'] = 0
            staff['total_floor_pay'] = 0
            staff['total_team_pay'] = 0
            staff['total_total_pay'] = 0
            event_staff = EventStaff.objects.filter(event__payroll_report=obj, user=staff['user']).order_by('user')
            for item in event_staff:
                if item.role == 's':
                    staff['total_stage_hours'] = staff['total_stage_hours'] + item.hours
                    staff['total_stage_hourly_pay'] = staff['total_stage_hourly_pay'] + item.hourly_pay
                    staff['total_stage_tip_pay'] = staff['total_stage_tip_pay'] + item.tip_pay
                    staff['total_stage_commission_pay'] = staff['total_stage_commission_pay'] + item.commission_pay
                    staff['total_stage_pay'] = staff['total_stage_hourly_pay'] + staff['total_stage_commission_pay'] + staff['total_stage_tip_pay']
                elif item.role == 'f':
                    staff['total_floor_hours'] = staff['total_floor_hours'] + item.hours
                    staff['total_floor_hourly_pay'] = staff['total_floor_hourly_pay'] + item.hourly_pay
                    staff['total_floor_tip_pay'] = staff['total_floor_tip_pay'] + item.tip_pay
                    staff['total_floor_commission_pay'] = staff['total_floor_commission_pay'] + item.commission_pay
                    staff['total_floor_pay'] = staff['total_floor_hourly_pay'] + staff['total_floor_commission_pay'] + staff['total_floor_tip_pay']
                elif item.role == 't':
                    staff['total_team_hours'] = staff['total_team_hours'] + item.hours
                    staff['total_team_hourly_pay'] = staff['total_team_hourly_pay'] + item.hourly_pay
                    staff['total_team_tip_pay'] = staff['total_team_tip_pay'] + item.tip_pay
                    staff['total_team_commission_pay'] = staff['total_team_commission_pay'] + item.commission_pay
                    staff['total_team_pay'] = staff['total_team_hourly_pay'] + staff['total_team_commission_pay'] + staff['total_team_tip_pay']
                staff['total_total_hours'] = staff['total_stage_hours'] + staff['total_floor_hours'] + staff['total_team_hours']
                staff['total_total_hourly_pay'] = staff['total_stage_hourly_pay'] + staff['total_floor_hourly_pay'] + staff['total_team_hourly_pay']
                staff['total_total_tip_pay'] = staff['total_stage_tip_pay'] + staff['total_floor_tip_pay'] + staff['total_team_tip_pay']
                staff['total_total_commission_pay'] = staff['total_stage_commission_pay'] + staff['total_floor_commission_pay'] + staff['total_team_commission_pay']
                staff['total_total_pay'] = staff['total_total_hourly_pay'] + staff['total_total_tip_pay'] + staff['total_total_commission_pay']
                staff['name'] = item.user.first_name + ' ' + item.user.last_name
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "distinct_users": distinct_users,
    }
    return render(request, "payroll/partials/perstaff-inline.html", context)
