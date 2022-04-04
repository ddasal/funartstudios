import decimal
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from events.models import AdminPay, Event, EventCustomer, EventStaff, EventTip, UserProfile
from activities.models import ActivityAdminPay, Activity, ActivityCustomer, ActivityStaff, ActivityTip
from products.models import Product, PurchaseItem, PurchaseOrder
from payroll.forms import ReportForm
from square.models import Square
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
            activities = Activity.objects.filter(payroll_report=parent_obj)
            for each in activities:
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
        square = Square.objects.filter(date__range=(obj.start_date, obj.end_date), tip__gt=0).order_by('date', 'time')
        square_tip_total = 0
        square_tip_total_reduced = 0
        for each in square:
            each.tip_reduced = round(Decimal(each.tip) * Decimal(.97), 2)
            square_tip_total = round(Decimal(square_tip_total) + Decimal(each.tip), 2)
        square_tip_total_reduced = round(Decimal(square_tip_total) * Decimal(0.97), 2)
        square_last_entry_date = Square.objects.latest('date', 'time')
        events = Event.objects.filter(date__range=(obj.start_date, obj.end_date)).order_by('date', 'time').annotate(worker_count=Count('eventstaff')).prefetch_related()
        activities = Activity.objects.filter(date__range=(obj.start_date, obj.end_date)).order_by('date', 'time').annotate(worker_count=Count('activitystaff')).prefetch_related()
        staff_count = EventStaff.objects.all().filter(event__payroll_report=obj).order_by('user').distinct('user').count()
        activity_staff_count = ActivityStaff.objects.all().filter(activity__payroll_report=obj).order_by('user').distinct('user').count()
        adminpay_count = AdminPay.objects.all().filter(event__payroll_report=obj).order_by('user').distinct('user').count()
        activityadminpay_count = ActivityAdminPay.objects.all().filter(activity__payroll_report=obj).order_by('user').distinct('user').count()
        payroll_gross = Decimal(0.0)
        events_without_workers = 0
        activities_without_workers = 0
        total_cx_hours = 0
        total_stage_hours = 0
        total_floor_hours = 0
        total_team_hours = 0
        total_total_hours = 0
        total_cx_hourly_pay = Decimal(0.0)
        total_stage_hourly_pay = Decimal(0.0)
        total_floor_hourly_pay = Decimal(0.0)
        total_team_hourly_pay = Decimal(0.0)
        total_total_hourly_pay = Decimal(0.0)
        total_cx_tip_pay = Decimal(0.0)
        total_stage_tip_pay = Decimal(0.0)
        total_floor_tip_pay = Decimal(0.0)
        total_team_tip_pay = Decimal(0.0)
        total_total_tip_pay = Decimal(0.0)
        total_total_tip_amount = Decimal(0.0)
        total_cx_commission_pay = Decimal(0.0)
        total_stage_commission_pay = Decimal(0.0)
        total_floor_commission_pay = Decimal(0.0)
        total_team_commission_pay = Decimal(0.0)
        total_total_commission_pay = Decimal(0.0)
        total_cx_pay = Decimal(0.0)
        total_stage_pay = Decimal(0.0)
        total_floor_pay = Decimal(0.0)
        total_team_pay = Decimal(0.0)
        total_admin_pay = Decimal(0.0)
        total_total_pay = Decimal(0.0)

        ## Events Pay
        for event in events:
            event.payroll_report = obj
            event.save()
            if event.worker_count == 0:
                events_without_workers = events_without_workers + 1
            tip_details = EventTip.objects.all().filter(event=event.id)
            event.count_stage = EventStaff.objects.all().filter(event=event.id, role='s').count()
            event.count_other = EventStaff.objects.all().filter(Q(role='f') | Q(role='t'), event=event.id).count()
            total_stage_tips = Decimal(0.0)
            total_floor_tips = Decimal(0.0)
            total_tips_amount = Decimal(0.0)
            if tip_details:
                for tip in tip_details:
                    total_stage_tips = total_stage_tips + tip.stage_amount
                    total_floor_tips = total_floor_tips + tip.floor_amount
                    total_tips_amount = total_tips_amount + tip.tip_amount
            event.total_stage_tips = total_stage_tips
            event.total_floor_tips = total_floor_tips
            event.total_total_tips = total_stage_tips + total_floor_tips
            event.total_total_tip_amount = total_tips_amount
            total_total_tip_amount = total_total_tip_amount + event.total_total_tip_amount
            if event.count_other == 0:
                if event.count_stage == 1:
                    update_tip_stage = EventStaff.objects.get(event=event.id, role='s')
                    total_stage_hours = total_stage_hours + update_tip_stage.hours
                    total_stage_hourly_pay = total_stage_hourly_pay + update_tip_stage.hourly_pay
                    total_stage_commission_pay = total_stage_commission_pay + update_tip_stage.prepaint_pay
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
                            total_stage_commission_pay = total_stage_commission_pay + staff.prepaint_pay
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
                    total_stage_commission_pay = total_stage_commission_pay + update_tip_stage.prepaint_pay
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
                            total_stage_commission_pay = total_stage_commission_pay + staff.prepaint_pay
                            staff.tip_pay = tip_each
                            total_stage_tip_pay = total_stage_tip_pay + staff.tip_pay
                            staff.save()
                if event.count_other == 1:
                    update_tip = EventStaff.objects.get(Q(role='f') | Q(role='t'), event=event.id)
                    update_tip.tip_pay = event.total_floor_tips
                    if update_tip.role == 'f':
                        total_floor_hours = total_floor_hours + update_tip.hours
                        total_floor_hourly_pay = total_floor_hourly_pay + update_tip.hourly_pay
                        total_floor_commission_pay = total_floor_commission_pay + update_tip.prepaint_pay
                        total_floor_tip_pay = total_floor_tip_pay + update_tip.tip_pay
                    elif update_tip.role == 't':
                        total_team_hours = total_team_hours + update_tip.hours
                        total_team_hourly_pay = total_team_hourly_pay + update_tip.hourly_pay
                        total_team_commission_pay = total_team_commission_pay + update_tip.prepaint_pay
                        total_team_tip_pay = total_team_tip_pay + update_tip.tip_pay
                    update_tip.save()
                elif event.count_other > 1:
                    tip_each = event.total_floor_tips / event.count_other
                    update_tip = EventStaff.objects.filter(Q(role='f') | Q(role='t'), event=event.id)
                    for staff in update_tip:
                        if staff.role == 'f':
                            total_floor_hours = total_floor_hours + staff.hours
                            total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                            total_floor_commission_pay = total_floor_commission_pay + staff.prepaint_pay
                        elif staff.role == 't':
                            total_team_hours = total_team_hours + staff.hours
                            total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                            total_team_commission_pay = total_team_commission_pay + staff.prepaint_pay
                        staff.tip_pay = tip_each
                        staff.save()
            admin_adj_pay = AdminPay.objects.filter(event=event.id)
            if admin_adj_pay:
                for admin_pay in admin_adj_pay:
                    total_admin_pay += Decimal(admin_pay.admin_pay)
            kit_sales = EventCustomer.objects.filter(event=event.id, type='h')
            if not kit_sales:
                update_commission = EventStaff.objects.filter(event=event.id)
                for staff in update_commission:
                    staff.commission_pay = Decimal(0.00)
                    staff.save()
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
        ### Activities Pay
        for activity in activities:
            activity.payroll_report = obj
            activity.save()
            if activity.worker_count == 0:
                activity_without_workers = activity_without_workers + 1
            tip_details = ActivityTip.objects.all().filter(activity=activity.id)
            activity.count_cx = ActivityStaff.objects.all().filter(activity=activity.id, role='c').count()
            activity.count_other = ActivityStaff.objects.all().filter(Q(role='f') | Q(role='t'), activity=activity.id).count()
            total_cx_tips = Decimal(0.0)
            total_floor_tips = Decimal(0.0)
            total_team_tips = Decimal(0.0)
            total_tips_amount = Decimal(0.0)
            if tip_details:
                for tip in tip_details:
                    if activity.type == 'c':
                        total_cx_tips = total_cx_tips + tip.staff_amount
                    elif activity.type == 't':
                        total_floor_tips = total_floor_tips + tip.staff_amount
                    elif activity.type == 'o':
                        total_team_tips = total_team_tips + tip.staff_amount
                    total_tips_amount = total_tips_amount + tip.staff_amount
            activity.total_cx_tips = total_cx_tips
            activity.total_floor_tips = total_floor_tips
            activity.total_team_tips = total_team_tips
            activity.total_total_tips = total_cx_tips + total_floor_tips + total_team_tips
            activity.total_total_tip_amount = total_tips_amount
            total_total_tip_amount = total_total_tip_amount + activity.total_total_tip_amount
            if activity.count_other == 0:
                if activity.count_cx == 1:
                    update_tip_cx = ActivityStaff.objects.get(activity=activity.id, role='c')
                    total_cx_hours = total_cx_hours + update_tip_cx.hours
                    total_cx_hourly_pay = total_cx_hourly_pay + update_tip_cx.hourly_pay
                    total_cx_commission_pay = total_cx_commission_pay + update_tip_cx.prepaint_pay
                    update_tip_cx.tip_pay = activity.total_total_tips
                    total_cx_tip_pay = total_cx_tip_pay + update_tip_cx.tip_pay
                    update_tip_cx.save()
                elif activity.count_cx > 1:
                    tip_each = activity.total_total_tips / activity.count_stage
                    update_tip = ActivityStaff.objects.filter(activity=activity.id)
                    for staff in update_tip:
                        if staff.role == 'c':
                            total_cx_hours = total_cx_hours + staff.hours
                            total_cx_hourly_pay = total_cx_hourly_pay + staff.hourly_pay
                            total_cx_commission_pay = total_cx_commission_pay + staff.prepaint_pay
                            staff.tip_pay = tip_each
                            total_cx_tip_pay = total_cx_tip_pay + staff.tip_pay
                            staff.save()
                elif activity.count_cx == 0: 
                    total_cx_tip_pay = total_cx_tip_pay + activity.total_total_tips
            if activity.count_other > 0:
                if activity.count_cx == 1:
                    update_tip_cx = ActivityStaff.objects.get(activity=activity.id, role='c')
                    total_cx_hours = total_cx_hours + update_tip_cx.hours
                    total_cx_hourly_pay = total_cx_hourly_pay + update_tip_cx.hourly_pay
                    total_cx_commission_pay = total_cx_commission_pay + update_tip_cx.prepaint_pay
                    update_tip_cx.tip_pay = activity.total_cx_tips
                    total_cx_tip_pay = total_cx_tip_pay + update_tip_cx.tip_pay
                    update_tip_cx.save()
                elif activity.count_cx > 1:
                    tip_each = activity.total_cx_tips / activity.count_cx
                    update_tip = ActivityStaff.objects.filter(activity=activity.id, role='c')
                    for staff in update_tip:
                        if staff.role == 'c':
                            total_cx_hours = total_cx_hours + staff.hours
                            total_cx_hourly_pay = total_cx_hourly_pay + staff.hourly_pay
                            total_cx_commission_pay = total_cx_commission_pay + staff.prepaint_pay
                            staff.tip_pay = tip_each
                            total_cx_tip_pay = total_cx_tip_pay + staff.tip_pay
                            staff.save()
                if activity.count_other == 1:
                    update_tip = ActivityStaff.objects.get(Q(role='f') | Q(role='t'), activity=activity.id)
                    update_tip.tip_pay = activity.total_floor_tips
                    if update_tip.role == 'f':
                        total_floor_hours = total_floor_hours + update_tip.hours
                        total_floor_hourly_pay = total_floor_hourly_pay + update_tip.hourly_pay
                        total_floor_commission_pay = total_floor_commission_pay + update_tip.prepaint_pay
                        total_floor_tip_pay = total_floor_tip_pay + update_tip.tip_pay
                    elif update_tip.role == 't':
                        total_team_hours = total_team_hours + update_tip.hours
                        total_team_hourly_pay = total_team_hourly_pay + update_tip.hourly_pay
                        total_team_commission_pay = total_team_commission_pay + update_tip.prepaint_pay
                        total_team_tip_pay = total_team_tip_pay + update_tip.tip_pay
                    update_tip.save()
                elif activity.count_other > 1:
                    tip_each = activity.total_floor_tips / activity.count_other
                    update_tip = ActivityStaff.objects.filter(Q(role='f') | Q(role='t'), activity=activity.id)
                    for staff in update_tip:
                        if staff.role == 'f':
                            total_floor_hours = total_floor_hours + staff.hours
                            total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                            total_floor_commission_pay = total_floor_commission_pay + staff.prepaint_pay
                        elif staff.role == 't':
                            total_team_hours = total_team_hours + staff.hours
                            total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                            total_team_commission_pay = total_team_commission_pay + staff.prepaint_pay
                        staff.tip_pay = tip_each
                        staff.save()
            admin_adj_pay = ActivityAdminPay.objects.filter(activity=activity.id)
            if admin_adj_pay:
                for admin_pay in admin_adj_pay:
                    total_admin_pay += Decimal(admin_pay.admin_pay)
            kit_sales = ActivityCustomer.objects.filter(activity=activity.id, type='h')
            if not kit_sales:
                update_commission = ActivityStaff.objects.filter(activity=activity.id)
                for staff in update_commission:
                    staff.commission_pay = Decimal(0.00)
                    staff.save()
            if kit_sales:
                kit_count = 0
                for kit in kit_sales:
                    kit_count = kit_count + kit.quantity
                if kit_count > 0:
                    activity.count_staff = int(activity.count_other) + int(activity.count_cx)
                    update_commission = ActivityStaff.objects.filter(activity=activity.id)
                    if activity.count_staff == 1:
                        for staff in update_commission:
                            staff.commission_pay = Decimal(0.00) * kit_count
                            staff.save()
                            if staff.role == 'c':
                                total_cx_commission_pay = total_cx_commission_pay + staff.commission_pay
                            elif staff.role == 'f':
                                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                            elif staff.role == 't':
                                total_team_commission_pay = total_team_commission_pay + staff.commission_pay
                    if activity.count_staff == 2:
                        for staff in update_commission:
                            staff.commission_pay = Decimal(0.00) * kit_count
                            staff.save()                        
                            if staff.role == 'c':
                                total_cx_commission_pay = total_cx_commission_pay + staff.commission_pay
                            elif staff.role == 'f':
                                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                            elif staff.role == 't':
                                total_team_commission_pay = total_team_commission_pay + staff.commission_pay
                    if activity.count_staff > 2:
                        for staff in update_commission:
                            staff.commission_pay = Decimal(0.00) * kit_count
                            staff.save()     
                            if staff.role == 'c':
                                total_cx_commission_pay = total_cx_commission_pay + staff.commission_pay
                            elif staff.role == 'f':
                                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay
                            elif staff.role == 't':
                                total_team_commission_pay = total_team_commission_pay + staff.commission_pay

        total_total_hours = total_stage_hours + total_floor_hours + total_team_hours + total_cx_hours
        total_total_hourly_pay = total_stage_hourly_pay + total_floor_hourly_pay + total_team_hourly_pay + total_cx_hourly_pay
        total_total_tip_pay = round(total_stage_tip_pay + total_floor_tip_pay + total_team_tip_pay + total_cx_tip_pay, 2)
        # total_total_tip_amount = total_stage_tip_pay + total_floor_tip_pay + total_team_tip_pay
        total_total_commission_pay = total_stage_commission_pay + total_floor_commission_pay + total_team_commission_pay + total_cx_commission_pay
        total_cx_pay = total_cx_hourly_pay + total_cx_tip_pay + total_cx_commission_pay
        total_stage_pay = total_stage_hourly_pay + total_stage_tip_pay + total_stage_commission_pay
        total_floor_pay = total_floor_hourly_pay + total_floor_tip_pay + total_floor_commission_pay
        total_team_pay = total_team_hourly_pay + total_team_tip_pay + total_team_commission_pay
        total_total_pay = total_stage_pay + total_floor_pay + total_team_pay + total_admin_pay + total_cx_pay
        obj.staff_count = staff_count
        obj.payroll_gross = total_total_pay
        obj.save()

        # if square_tip_total_reduced == total_total_tip_pay:
        #     sq_matches = True
        # else:
        #     sq_matches = False
        if square_tip_total == total_total_tip_amount:
            sq_matches = True
        else:
            sq_matches = False

    except:
        obj = None
    if obj is None:
        return HttpResponse('Not found')
    context = {
        "object": obj,
        "events": events,
        "activities": activities,
        "hx_url": hx_url,
        "payroll_gross": payroll_gross,
        "events_without_workers": events_without_workers,
        "activities_without_workers": activities_without_workers,
        "total_cx_hours": total_cx_hours,
        "total_stage_hours": total_stage_hours,
        "total_floor_hours": total_floor_hours,
        "total_team_hours": total_team_hours,
        "total_total_hours": total_total_hours,
        "total_cx_hourly_pay": total_cx_hourly_pay,
        "total_stage_hourly_pay": total_stage_hourly_pay,
        "total_floor_hourly_pay": total_floor_hourly_pay,
        "total_team_hourly_pay": total_team_hourly_pay,
        "total_total_hourly_pay": total_total_hourly_pay,
        "total_cx_tip_pay": total_cx_tip_pay,
        "total_stage_tip_pay": total_stage_tip_pay,
        "total_floor_tip_pay": total_floor_tip_pay,
        "total_team_tip_pay": total_team_tip_pay,
        "total_total_tip_pay": total_total_tip_pay,
        "total_cx_commission_pay": total_cx_commission_pay,
        "total_stage_commission_pay": total_stage_commission_pay,
        "total_floor_commission_pay": total_floor_commission_pay,
        "total_team_commission_pay": total_team_commission_pay,
        "total_total_commission_pay": total_total_commission_pay,
        "total_cx_pay": total_cx_pay,
        "total_stage_pay": total_stage_pay,
        "total_floor_pay": total_floor_pay,
        "total_team_pay": total_team_pay,
        "total_total_pay": total_total_pay,
        "square": square,
        "square_last_entry_date": square_last_entry_date,
        "square_tip_total_reduced": square_tip_total_reduced,
        "square_tip_total": square_tip_total,
        "total_admin_pay": total_admin_pay,
        "sq_matches": sq_matches,
        "total_total_tip_amount": total_total_tip_amount
    }
    return render(request, "payroll/partials/detail.html", context)
 


@permission_required('payroll.add_report')
def report_create_view(request):
    last_report = PayReport.objects.all().order_by('-end_date').first()
    new_start = last_report.end_date + timedelta(days=1)
    new_end = new_start + timedelta(days=13)
    new_payday = new_end + timedelta(days=5)
    initial_form_data = {'start_date': new_start, 'end_date': new_end, 'pay_date': new_payday}
    form = ReportForm(request.POST or None, initial=initial_form_data)
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
            adminpay = AdminPay.objects.filter(event=event.id)
            tips = EventTip.objects.filter(event=event.id)
            for each in staff:
                each.status = 'c'
                each.save()
            for each in adminpay:
                each.status = 'c'
                each.save()
            for each in tips:
                each.status = 'c'
                each.save()

        children_activity = Activity.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for activity in children_activity:
            activity.payroll_status = 'c'
            activity.save()
            staff = ActivityStaff.objects.filter(activity=activity.id)
            adminpay = ActivityAdminPay.objects.filter(activity=activity.id)
            tips = ActivityTip.objects.filter(activity=activity.id)
            for each in staff:
                each.status = 'c'
                each.save()
            for each in adminpay:
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
            adminpay = AdminPay.objects.filter(event=event.id)
            tips = EventTip.objects.filter(event=event.id)
            for each in staff:
                each.status = 'p'
                each.save()
            for each in adminpay:
                each.status = 'p'
                each.save()
            for each in tips:
                each.status = 'p'
                each.save()

        children_activity = Activity.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for activity in children_activity:
            activity.payroll_status = 'p'
            activity.save()
            staff = ActivityStaff.objects.filter(activity=activity.id)
            adminpay = ActivityAdminPay.objects.filter(activity=activity.id)
            tips = ActivityTip.objects.filter(activity=activity.id)
            for each in staff:
                each.status = 'p'
                each.save()
            for each in adminpay:
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
        events = Event.objects.all().filter(payroll_report=obj).order_by('date', 'time').prefetch_related()
        activities = Activity.objects.all().filter(payroll_report=obj).order_by('date', 'time').prefetch_related()
        event_staff = EventStaff.objects.all().filter(event__payroll_report=obj, user=request.user.id).order_by('date')
        activity_staff = ActivityStaff.objects.all().filter(activity__payroll_report=obj, user=request.user.id).order_by('date')
        admin_pay = AdminPay.objects.all().filter(event__payroll_report=obj, user=request.user.id).order_by('date')
        activity_admin_pay = ActivityAdminPay.objects.all().filter(activity__payroll_report=obj, user=request.user.id).order_by('date')
        admin_pay_include = False
        activity_admin_pay_include = False
        if admin_pay:
            admin_pay_include = True
        if activity_admin_pay:
            activity_admin_pay_include = True
        total_stage_hours = 0
        total_cx_hours = 0
        total_floor_hours = 0
        total_team_hours = 0
        total_total_hours = 0
        total_stage_hourly_pay = Decimal(0.0)
        total_cx_hourly_pay = Decimal(0.0)
        total_floor_hourly_pay = Decimal(0.0)
        total_team_hourly_pay = Decimal(0.0)
        total_total_hourly_pay = Decimal(0.0)
        total_stage_tip_pay = Decimal(0.0)
        total_cx_tip_pay = Decimal(0.0)
        total_floor_tip_pay = Decimal(0.0)
        total_team_tip_pay = Decimal(0.0)
        total_total_tip_pay = Decimal(0.0)
        total_stage_commission_pay = Decimal(0.0)
        total_cx_commission_pay = Decimal(0.0)
        total_floor_commission_pay = Decimal(0.0)
        total_team_commission_pay = Decimal(0.0)
        total_total_commission_pay = Decimal(0.0)
        total_stage_pay = Decimal(0.0)
        total_cx_pay = Decimal(0.0)
        total_floor_pay = Decimal(0.0)
        total_team_pay = Decimal(0.0)
        total_total_pay = Decimal(0.0)
        total_admin_pay = Decimal(0.0)
        for item in admin_pay:
            total_admin_pay += Decimal(item.admin_pay)
        for item in activity_admin_pay:
            total_admin_pay += Decimal(item.admin_pay)

        for staff in event_staff:
            if staff.role == 's':
                total_stage_hours = total_stage_hours + staff.hours
                total_stage_hourly_pay = total_stage_hourly_pay + staff.hourly_pay
                total_stage_tip_pay = total_stage_tip_pay + staff.tip_pay
                total_stage_commission_pay = total_stage_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_stage_pay = total_stage_hourly_pay + total_stage_commission_pay + total_stage_tip_pay
            elif staff.role == 'f':
                total_floor_hours = total_floor_hours + staff.hours
                total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                total_floor_tip_pay = total_floor_tip_pay + staff.tip_pay
                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_floor_pay = total_floor_hourly_pay + total_floor_commission_pay + total_floor_tip_pay
            elif staff.role == 't':
                total_team_hours = total_team_hours + staff.hours
                total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                total_team_tip_pay = total_team_tip_pay + staff.tip_pay
                total_team_commission_pay = total_team_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_team_pay = total_team_hourly_pay + total_team_commission_pay + total_team_tip_pay

        for staff in activity_staff:
            if staff.role == 'c':
                total_cx_hours = total_cx_hours + staff.hours
                total_cx_hourly_pay = total_cx_hourly_pay + staff.hourly_pay
                total_cx_tip_pay = total_cx_tip_pay + staff.tip_pay
                total_cx_commission_pay = total_cx_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_cx_pay = total_cx_hourly_pay + total_cx_commission_pay + total_cx_tip_pay
            elif staff.role == 'f':
                total_floor_hours = total_floor_hours + staff.hours
                total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                total_floor_tip_pay = total_floor_tip_pay + staff.tip_pay
                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_floor_pay = total_floor_hourly_pay + total_floor_commission_pay + total_floor_tip_pay
            elif staff.role == 't':
                total_team_hours = total_team_hours + staff.hours
                total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                total_team_tip_pay = total_team_tip_pay + staff.tip_pay
                total_team_commission_pay = total_team_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_team_pay = total_team_hourly_pay + total_team_commission_pay + total_team_tip_pay


        total_total_hours = total_stage_hours + total_floor_hours + total_team_hours + total_cx_hours
        total_total_hourly_pay = total_stage_hourly_pay + total_floor_hourly_pay + total_team_hourly_pay + total_cx_hourly_pay
        total_total_tip_pay = total_stage_tip_pay + total_floor_tip_pay + total_team_tip_pay + total_cx_tip_pay
        total_total_commission_pay = total_stage_commission_pay + total_floor_commission_pay + total_team_commission_pay + total_cx_commission_pay
        total_total_pay = total_stage_pay + total_floor_pay + total_team_pay + total_admin_pay + total_cx_pay

    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "event_staff": event_staff,
        "activity_staff": activity_staff,
        "total_stage_hours": total_stage_hours,
        "total_cx_hours": total_cx_hours,
        "total_floor_hours": total_floor_hours,
        "total_team_hours": total_team_hours,
        "total_total_hours": total_total_hours,
        "total_stage_hourly_pay": total_stage_hourly_pay,
        "total_cx_hourly_pay": total_cx_hourly_pay,
        "total_floor_hourly_pay": total_floor_hourly_pay,
        "total_team_hourly_pay": total_team_hourly_pay,
        "total_total_hourly_pay": total_total_hourly_pay,
        "total_stage_tip_pay": total_stage_tip_pay,
        "total_cx_tip_pay": total_cx_tip_pay,
        "total_floor_tip_pay": total_floor_tip_pay,
        "total_team_tip_pay": total_team_tip_pay,
        "total_total_tip_pay": total_total_tip_pay,
        "total_stage_commission_pay": total_stage_commission_pay,
        "total_cx_commission_pay": total_cx_commission_pay,
        "total_floor_commission_pay": total_floor_commission_pay,
        "total_team_commission_pay": total_team_commission_pay,
        "total_total_commission_pay": total_total_commission_pay,
        "total_stage_pay": total_stage_pay,
        "total_cx_pay": total_cx_pay,
        "total_floor_pay": total_floor_pay,
        "total_team_pay": total_team_pay,
        "total_admin_pay": total_admin_pay,
        "admin_pay_include": admin_pay_include,
        "activity_admin_pay_include": activity_admin_pay_include,
        "total_total_pay": total_total_pay
    }
    return render(request, "payroll/partials/staff-detail.html", context)
 

@login_required
def report_staff_list_view(request):
    qs1 = PayReport.objects.filter(Q(event__eventstaff__user=request.user.id) | Q(activity__activitystaff__user=request.user.id) | Q(event__adminpay__user=request.user.id) | Q(activity__activityadminpay__user=request.user.id)).order_by('-start_date').distinct()
    page = request.GET.get('page', 1)

    paginator = Paginator(qs1, 10)
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
def report_staff_mgmt_detail_view(request, id=None, staff_id=None):
    hx_url = reverse("payroll:hx-staff-mgmt-detail", kwargs={"id": id, "staff_id": staff_id})
    report_obj = PayReport.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "report_obj": report_obj
    }
    return render(request, "payroll/staff-detail.html", context)

@permission_required('payroll.change_report')
def report_staff_detail_mgmt_hx_view(request, id=None, staff_id=None):
    try:
        obj = PayReport.objects.get(id=id)
        events = Event.objects.all().filter(payroll_report=obj).order_by('date', 'time').prefetch_related()
        activities = Activity.objects.all().filter(payroll_report=obj).order_by('date', 'time').prefetch_related()
        event_staff = EventStaff.objects.all().filter(event__payroll_report=obj, user=staff_id).order_by('date')
        activity_staff = ActivityStaff.objects.all().filter(activity__payroll_report=obj, user=staff_id).order_by('date')
        admin_pay = AdminPay.objects.all().filter(event__payroll_report=obj, user=staff_id).order_by('date')
        activity_admin_pay = ActivityAdminPay.objects.all().filter(activity__payroll_report=obj, user=staff_id).order_by('date')
        admin_pay_include = False
        if admin_pay:
            admin_pay_include = True
        activity_admin_pay_include = False
        if activity_admin_pay:
            activity_admin_pay_include = True
        report_staff = UserProfile.objects.get(user_id=staff_id)
        total_stage_hours = 0
        total_cx_hours = 0
        total_floor_hours = 0
        total_team_hours = 0
        total_total_hours = 0
        total_stage_hourly_pay = Decimal(0.0)
        total_cx_hourly_pay = Decimal(0.0)
        total_floor_hourly_pay = Decimal(0.0)
        total_team_hourly_pay = Decimal(0.0)
        total_total_hourly_pay = Decimal(0.0)
        total_stage_tip_pay = Decimal(0.0)
        total_cx_tip_pay = Decimal(0.0)
        total_floor_tip_pay = Decimal(0.0)
        total_team_tip_pay = Decimal(0.0)
        total_total_tip_pay = Decimal(0.0)
        total_stage_commission_pay = Decimal(0.0)
        total_cx_commission_pay = Decimal(0.0)
        total_floor_commission_pay = Decimal(0.0)
        total_team_commission_pay = Decimal(0.0)
        total_total_commission_pay = Decimal(0.0)
        total_stage_pay = Decimal(0.0)
        total_cx_pay = Decimal(0.0)
        total_floor_pay = Decimal(0.0)
        total_team_pay = Decimal(0.0)
        total_total_pay = Decimal(0.0)
        total_admin_pay = Decimal(0.0)
        for item in admin_pay:
            total_admin_pay += Decimal(item.admin_pay)
        for item in activity_admin_pay:
            total_admin_pay += Decimal(item.admin_pay)

        for staff in event_staff:
            if staff.role == 's':
                total_stage_hours = total_stage_hours + staff.hours
                total_stage_hourly_pay = total_stage_hourly_pay + staff.hourly_pay
                total_stage_tip_pay = total_stage_tip_pay + staff.tip_pay
                total_stage_commission_pay = total_stage_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_stage_pay = total_stage_hourly_pay + total_stage_commission_pay + total_stage_tip_pay
            elif staff.role == 'f':
                total_floor_hours = total_floor_hours + staff.hours
                total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                total_floor_tip_pay = total_floor_tip_pay + staff.tip_pay
                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_floor_pay = total_floor_hourly_pay + total_floor_commission_pay + total_floor_tip_pay
            elif staff.role == 't':
                total_team_hours = total_team_hours + staff.hours
                total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                total_team_tip_pay = total_team_tip_pay + staff.tip_pay
                total_team_commission_pay = total_team_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_team_pay = total_team_hourly_pay + total_team_commission_pay + total_team_tip_pay

        for staff in activity_staff:
            if staff.role == 'c':
                total_cx_hours = total_cx_hours + staff.hours
                total_cx_hourly_pay = total_cx_hourly_pay + staff.hourly_pay
                total_cx_tip_pay = total_cx_tip_pay + staff.tip_pay
                total_cx_commission_pay = total_cx_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_cx_pay = total_cx_hourly_pay + total_cx_commission_pay + total_cx_tip_pay
            elif staff.role == 'f':
                total_floor_hours = total_floor_hours + staff.hours
                total_floor_hourly_pay = total_floor_hourly_pay + staff.hourly_pay
                total_floor_tip_pay = total_floor_tip_pay + staff.tip_pay
                total_floor_commission_pay = total_floor_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_floor_pay = total_floor_hourly_pay + total_floor_commission_pay + total_floor_tip_pay
            elif staff.role == 't':
                total_team_hours = total_team_hours + staff.hours
                total_team_hourly_pay = total_team_hourly_pay + staff.hourly_pay
                total_team_tip_pay = total_team_tip_pay + staff.tip_pay
                total_team_commission_pay = total_team_commission_pay + staff.commission_pay + staff.prepaint_pay
                total_team_pay = total_team_hourly_pay + total_team_commission_pay + total_team_tip_pay

        total_total_hours = total_stage_hours + total_floor_hours + total_team_hours + total_cx_hours
        total_total_hourly_pay = total_stage_hourly_pay + total_floor_hourly_pay + total_team_hourly_pay + total_cx_hourly_pay
        total_total_tip_pay = total_stage_tip_pay + total_floor_tip_pay + total_team_tip_pay + total_cx_tip_pay
        total_total_commission_pay = total_stage_commission_pay + total_floor_commission_pay + total_team_commission_pay + total_cx_commission_pay
        total_total_pay = total_stage_pay + total_floor_pay + total_team_pay + total_admin_pay + total_cx_pay

    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "event_staff": event_staff,
        "activity_staff": activity_staff,
        "report_staff": report_staff,
        "total_stage_hours": total_stage_hours,
        "total_cx_hours": total_cx_hours,
        "total_floor_hours": total_floor_hours,
        "total_team_hours": total_team_hours,
        "total_total_hours": total_total_hours,
        "total_stage_hourly_pay": total_stage_hourly_pay,
        "total_cx_hourly_pay": total_cx_hourly_pay,
        "total_floor_hourly_pay": total_floor_hourly_pay,
        "total_team_hourly_pay": total_team_hourly_pay,
        "total_total_hourly_pay": total_total_hourly_pay,
        "total_stage_tip_pay": total_stage_tip_pay,
        "total_cx_tip_pay": total_cx_tip_pay,
        "total_floor_tip_pay": total_floor_tip_pay,
        "total_team_tip_pay": total_team_tip_pay,
        "total_total_tip_pay": total_total_tip_pay,
        "total_stage_commission_pay": total_stage_commission_pay,
        "total_cx_commission_pay": total_cx_commission_pay,
        "total_floor_commission_pay": total_floor_commission_pay,
        "total_team_commission_pay": total_team_commission_pay,
        "total_total_commission_pay": total_total_commission_pay,
        "total_stage_pay": total_stage_pay,
        "total_cx_pay": total_cx_pay,
        "total_floor_pay": total_floor_pay,
        "total_team_pay": total_team_pay,
        "total_admin_pay": total_admin_pay,
        "admin_pay_include": admin_pay_include,
        "activity_admin_pay_include": activity_admin_pay_include,
        "total_total_pay": total_total_pay
    }
    return render(request, "payroll/partials/staff-mgmt-detail.html", context)



@permission_required('payroll.change_report')
def report_staff_summary_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = PayReport.objects.get(id=id)
        eventstaff_list = EventStaff.objects.filter(event__payroll_report=obj)
        activitystaff_list = ActivityStaff.objects.filter(activity__payroll_report=obj)
        adminpay_list = AdminPay.objects.filter(event__payroll_report=obj)
        activity_adminpay_list = ActivityAdminPay.objects.filter(activity__payroll_report=obj)
        distinct_users = list(eventstaff_list.values('user').distinct()) #.exclude(Q(user=7) | Q(user=1))
        activity_distinct_users = list(activitystaff_list.values('user').distinct()) #.exclude(Q(user=7) | Q(user=1))
        adminpay_users = list(adminpay_list.values('user').distinct()) #.exclude(Q(user=7) | Q(user=1))
        activity_adminpay_users = list(activity_adminpay_list.values('user').distinct()) #.exclude(Q(user=7) | Q(user=1))
        combined_users = distinct_users + adminpay_users + activity_distinct_users + activity_adminpay_users
        res = set(val for dic in combined_users for val in dic.values())
        unique_ids = []
        for each in res:
            unique_ids.append({'user': each})
        for staff in unique_ids:
            staff['total_stage_hours'] = 0
            staff['total_cx_hours'] = 0
            staff['total_floor_hours'] = 0
            staff['total_team_hours'] = 0
            staff['total_total_hours'] = 0
            staff['total_stage_hourly_pay'] = Decimal(0.0)
            staff['total_cx_hourly_pay'] = Decimal(0.0)
            staff['total_floor_hourly_pay'] = Decimal(0.0)
            staff['total_team_hourly_pay'] = Decimal(0.0)
            staff['total_total_hourly_pay'] = Decimal(0.0)
            staff['total_stage_tip_pay'] = Decimal(0.0)
            staff['total_cx_tip_pay'] = Decimal(0.0)
            staff['total_floor_tip_pay'] = Decimal(0.0)
            staff['total_team_tip_pay'] = Decimal(0.0)
            staff['total_total_tip_pay'] = Decimal(0.0)
            staff['total_stage_commission_pay'] = Decimal(0.0)
            staff['total_cx_commission_pay'] = Decimal(0.0)
            staff['total_floor_commission_pay'] = Decimal(0.0)
            staff['total_team_commission_pay'] = Decimal(0.0)
            staff['total_total_commission_pay'] = Decimal(0.0)
            staff['total_stage_pay'] = Decimal(0.0)
            staff['total_cx_pay'] = Decimal(0.0)
            staff['total_floor_pay'] = Decimal(0.0)
            staff['total_team_pay'] = Decimal(0.0)
            staff['total_total_pay'] = Decimal(0.0)
            staff['total_admin_pay'] = Decimal(0.0)
            event_staff = EventStaff.objects.filter(event__payroll_report=obj, user=staff['user']).order_by('user')
            activity_staff = ActivityStaff.objects.filter(activity__payroll_report=obj, user=staff['user']).order_by('user')
            admin_pay = AdminPay.objects.filter(event__payroll_report=obj, user=staff['user']).order_by('user')
            activity_admin_pay = ActivityAdminPay.objects.filter(activity__payroll_report=obj, user=staff['user']).order_by('user')
            for item in admin_pay:
                staff['total_admin_pay'] += Decimal(item.admin_pay)
                staff['total_total_pay'] += staff['total_admin_pay']
                staff['name'] = item.user.first_name + ' ' + item.user.last_name
            for item in activity_admin_pay:
                staff['total_admin_pay'] += Decimal(item.admin_pay)
                staff['total_total_pay'] += staff['total_admin_pay']
                staff['name'] = item.user.first_name + ' ' + item.user.last_name

            for item in event_staff:
                if item.role == 's':
                    staff['rate_stage'] = item.rate
                    staff['total_stage_hours'] = staff['total_stage_hours'] + item.hours
                    staff['total_stage_hourly_pay'] = staff['total_stage_hourly_pay'] + item.hourly_pay
                    staff['total_stage_tip_pay'] = staff['total_stage_tip_pay'] + item.tip_pay
                    staff['total_stage_commission_pay'] = staff['total_stage_commission_pay'] + item.commission_pay + item.prepaint_pay
                    staff['total_stage_pay'] = staff['total_stage_hourly_pay'] + staff['total_stage_commission_pay'] + staff['total_stage_tip_pay']
                elif item.role == 'f':
                    staff['rate_floor'] = item.rate
                    staff['total_floor_hours'] = staff['total_floor_hours'] + item.hours
                    staff['total_floor_hourly_pay'] = staff['total_floor_hourly_pay'] + item.hourly_pay
                    staff['total_floor_tip_pay'] = staff['total_floor_tip_pay'] + item.tip_pay
                    staff['total_floor_commission_pay'] = staff['total_floor_commission_pay'] + item.commission_pay + item.prepaint_pay
                    staff['total_floor_pay'] = staff['total_floor_hourly_pay'] + staff['total_floor_commission_pay'] + staff['total_floor_tip_pay']
                elif item.role == 't':
                    staff['rate_team'] = item.rate
                    staff['total_team_hours'] = staff['total_team_hours'] + item.hours
                    staff['total_team_hourly_pay'] = staff['total_team_hourly_pay'] + item.hourly_pay
                    staff['total_team_tip_pay'] = staff['total_team_tip_pay'] + item.tip_pay
                    staff['total_team_commission_pay'] = staff['total_team_commission_pay'] + item.commission_pay + item.prepaint_pay
                    staff['total_team_pay'] = staff['total_team_hourly_pay'] + staff['total_team_commission_pay'] + staff['total_team_tip_pay']

                staff['total_total_hours'] = staff['total_stage_hours'] + staff['total_floor_hours'] + staff['total_team_hours']
                staff['total_total_hourly_pay'] = staff['total_stage_hourly_pay'] + staff['total_floor_hourly_pay'] + staff['total_team_hourly_pay']
                staff['total_total_tip_pay'] = staff['total_stage_tip_pay'] + staff['total_floor_tip_pay'] + staff['total_team_tip_pay']
                staff['total_total_commission_pay'] = staff['total_stage_commission_pay'] + staff['total_floor_commission_pay'] + staff['total_team_commission_pay']
                staff['total_total_pay'] = staff['total_total_hourly_pay'] + staff['total_total_tip_pay'] + staff['total_total_commission_pay'] + staff['total_admin_pay']
                staff['name'] = item.user.first_name + ' ' + item.user.last_name

            for item in activity_staff:
                if item.role == 'c':
                    staff['rate_cx'] = item.rate
                    staff['total_cx_hours'] = staff['total_cx_hours'] + item.hours
                    staff['total_cx_hourly_pay'] = staff['total_cx_hourly_pay'] + item.hourly_pay
                    staff['total_cx_tip_pay'] = staff['total_cx_tip_pay'] + item.tip_pay
                    staff['total_cx_commission_pay'] = staff['total_cx_commission_pay'] + item.commission_pay + item.prepaint_pay
                    staff['total_cx_pay'] = staff['total_cx_hourly_pay'] + staff['total_cx_commission_pay'] + staff['total_cx_tip_pay']
                elif item.role == 'f':
                    staff['rate_floor'] = item.rate
                    staff['total_floor_hours'] = staff['total_floor_hours'] + item.hours
                    staff['total_floor_hourly_pay'] = staff['total_floor_hourly_pay'] + item.hourly_pay
                    staff['total_floor_tip_pay'] = staff['total_floor_tip_pay'] + item.tip_pay
                    staff['total_floor_commission_pay'] = staff['total_floor_commission_pay'] + item.commission_pay + item.prepaint_pay
                    staff['total_floor_pay'] = staff['total_floor_hourly_pay'] + staff['total_floor_commission_pay'] + staff['total_floor_tip_pay']
                elif item.role == 't':
                    staff['rate_team'] = item.rate
                    staff['total_team_hours'] = staff['total_team_hours'] + item.hours
                    staff['total_team_hourly_pay'] = staff['total_team_hourly_pay'] + item.hourly_pay
                    staff['total_team_tip_pay'] = staff['total_team_tip_pay'] + item.tip_pay
                    staff['total_team_commission_pay'] = staff['total_team_commission_pay'] + item.commission_pay + item.prepaint_pay
                    staff['total_team_pay'] = staff['total_team_hourly_pay'] + staff['total_team_commission_pay'] + staff['total_team_tip_pay']

                staff['total_total_hours'] = staff['total_stage_hours'] + staff['total_cx_hours'] + staff['total_floor_hours'] + staff['total_team_hours']
                staff['total_total_hourly_pay'] = staff['total_stage_hourly_pay'] + staff['total_cx_hourly_pay'] + staff['total_floor_hourly_pay'] + staff['total_team_hourly_pay']
                staff['total_total_tip_pay'] = staff['total_stage_tip_pay'] + staff['total_cx_tip_pay'] + staff['total_floor_tip_pay'] + staff['total_team_tip_pay']
                staff['total_total_commission_pay'] = staff['total_stage_commission_pay'] + staff['total_cx_commission_pay'] + staff['total_floor_commission_pay'] + staff['total_team_commission_pay']
                staff['total_total_pay'] = staff['total_total_hourly_pay'] + staff['total_total_tip_pay'] + staff['total_total_commission_pay'] + staff['total_admin_pay']
                staff['name'] = item.user.first_name + ' ' + item.user.last_name

    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "distinct_users": unique_ids,
    }
    return render(request, "payroll/partials/perstaff-inline.html", context)
