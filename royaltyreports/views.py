import decimal
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from events.models import Event, EventCustomer, EventStaff
from products.models import Product, PurchaseItem, PurchaseOrder
from royaltyreports.forms import ReportForm
from django.db.models import Q
from royaltyreports.models import RoyaltyReport
from square.models import Square
from decimal import Decimal

# Create your views here.

@permission_required('royaltyreports.view_report')
def report_list_view(request):
    qs = RoyaltyReport.objects.all().order_by('-start_date')
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
    return render(request, "royaltyreports/list.html", context)

@permission_required('royaltyreports.view_report')
def report_detail_view(request, id=None):
    hx_url = reverse("royalty:hx-detail", kwargs={"id": id})
    report_obj = RoyaltyReport.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "report_obj": report_obj
    }
    return render(request, "royaltyreports/detail.html", context)


@permission_required('royaltyreports.delete_report')
def report_delete_view(request, id=None):
    try:
        obj = RoyaltyReport.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            parent_obj = obj
            events = Event.objects.filter(royalty_report=parent_obj)
            for each in events:
                each.royalty_report = None
                each.save()
            obj.delete()
            success_url = reverse('royalty:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)
        else:
            success_url = reverse('royalty:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url,
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "royaltyreports/delete.html", context)


@permission_required('royaltyreports.view_report')
def report_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = RoyaltyReport.objects.get(id=id)
        events = Event.objects.filter(Q(type='s') | Q(type='p') | Q(type='w') | Q(type='t'), date__range=(obj.start_date, obj.end_date)).order_by('date', 'time').prefetch_related()
        kits = Event.objects.filter(Q(type='s') | Q(type='p') | Q(type='w') | Q(type='t') | Q(type='r'), date__range=(obj.start_date, obj.end_date)).order_by('date', 'time').prefetch_related()
        sqaure_info = Square.objects.filter(date__range=(obj.start_date, obj.end_date)).exclude(Q(description__icontains='Twist at Home Kit') | Q(description__icontains='Event'))
        square_last_entry_date = Square.objects.latest('date', 'time')
        report_adjusted_gross_revenue = Decimal(0.0)
        report_gross_revenue = Decimal(0.0)
        report_adjustments = Decimal(0.0)
        report_net_revenue = Decimal(0.0)
        report_royalty = Decimal(0.0)
        report_ad_funds = Decimal(0.0)
        report_seats = 0
        report_kits = 0
        kit_gross_revenue = Decimal(0.0)
        kit_adjustments = Decimal(0.0)
        report_surface_count = 0
        report_square_sales = Decimal(0.0)
        for each in events:
            each.temp_customer_seats = 0
            temp_customer_seats = [int(each.quantity) for each in EventCustomer.objects.filter(event=each.id, type='r')]
            each.temp_customer_seats = sum(temp_customer_seats)
            report_seats = report_seats + each.temp_customer_seats

            each.temp_gross_revenue = Decimal(0.0)
            temp_gross_revenue = [Decimal(each.total_price) for each in EventCustomer.objects.filter(event=each.id, type='r')]
            each.temp_gross_revenue = sum(temp_gross_revenue)
            report_gross_revenue = report_gross_revenue + each.temp_gross_revenue

            each.temp_adjustments = Decimal(0.0)
            temp_adjustments = [Decimal(each.taxes) for each in EventCustomer.objects.filter(event=each.id, type='r')]
            each.temp_adjustments = sum(temp_adjustments)
            report_adjustments = report_adjustments + each.temp_adjustments

            each.temp_cost_factors = Decimal(0.0)
            temp_cost_factors = [Decimal(each.cost_factor) for each in EventCustomer.objects.filter(event=each.id, type='r')]
            each.temp_cost_factors = sum(temp_cost_factors)

        for each in kits:
            each.temp_customer_seats = 0
            temp_customer_seats = [int(each.quantity) for each in EventCustomer.objects.filter(event=each.id, type='h')]
            each.temp_customer_seats = sum(temp_customer_seats)
            report_kits = report_kits + each.temp_customer_seats

            each.temp_gross_revenue = Decimal(0.0)
            temp_gross_revenue = [Decimal(each.total_price) for each in EventCustomer.objects.filter(event=each.id, type='h')]
            each.temp_gross_revenue = sum(temp_gross_revenue)
            kit_gross_revenue = kit_gross_revenue + each.temp_gross_revenue

            each.temp_adjustments = Decimal(0.0)
            temp_adjustments = [Decimal(each.taxes) for each in EventCustomer.objects.filter(event=each.id, type='h')]
            each.temp_adjustments = sum(temp_adjustments)
            kit_adjustments = kit_adjustments + each.temp_adjustments

            each.temp_cost_factors = Decimal(0.0)
            temp_cost_factors = [Decimal(each.cost_factor) for each in EventCustomer.objects.filter(event=each.id, type='h')]
            each.temp_cost_factors = sum(temp_cost_factors)


        pi_qs = PurchaseItem.objects.filter(date__lte=obj.end_date)
        inventory_total = 0
        for each in pi_qs:
            each.temp_received_quantity = 0
            each.temp_received_quantity = int(each.received_quantity)
            inventory_total = inventory_total + each.temp_received_quantity

        event_qs = Event.objects.filter(date__lte=obj.end_date)
        
        for item in event_qs:
            item.temp_customer_used = 0
            temp_customer_each = [int(item.total_customer_qty) for item in EventCustomer.objects.filter(event=item.id)]
            item.temp_customer_used = sum(temp_customer_each)

            item.temp_prepaint_used = 0
            temp_prepaint_each = [int(item.prepaint_qty) for item in EventStaff.objects.filter(event=item.id)]
            item.temp_prepaint_used = sum(temp_prepaint_each)

            item.temp_event_used = 0
            temp_event_each = [int(item.event_qty) for item in EventStaff.objects.filter(event=item.id)]
            item.temp_event_used = sum(temp_event_each)


            inventory_total = inventory_total - item.temp_customer_used - item.temp_prepaint_used - item.temp_event_used
            report_surface_count = report_surface_count + item.temp_customer_used + item.temp_prepaint_used + item.temp_event_used

        for sq in sqaure_info:
            report_square_sales = report_square_sales + sq.gross_sales

        report_adjusted_gross_revenue = Decimal(report_gross_revenue) + Decimal(kit_gross_revenue)
        report_net_revenue = Decimal(report_adjusted_gross_revenue) - Decimal(report_adjustments)
        report_royalty = Decimal(report_net_revenue) * Decimal(.06)
        report_ad_funds = Decimal(report_net_revenue) * Decimal(.02)
        
        obj.adjusted_gross_revenue = report_adjusted_gross_revenue
        obj.adjustments = report_adjustments
        obj.net_revenue = report_net_revenue
        obj.royalty = report_royalty
        obj.ad_funds = report_ad_funds
        obj.reservations = report_seats
        obj.surface_count = int(inventory_total)
        obj.kits = report_kits
        obj.square_retail_sales = report_square_sales
        obj.save()
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "events": events,
        "report_seats": report_seats,
        "report_gross_revenue": report_gross_revenue,
        "report_adjustments": report_adjustments,
        "inventory_total": inventory_total,
        "report_kits": report_kits,
        "kit_gross_revenue": kit_gross_revenue,
        "kit_adjustments": kit_adjustments,
        "report_adjusted_gross_revenue": report_adjusted_gross_revenue,
        "report_net_revenue": report_net_revenue,
        "report_royalty": report_royalty,
        "report_ad_funds": report_ad_funds,
        "report_square_sales": report_square_sales,
        "report_surface_count": report_surface_count,
        "square_last_entry_date": square_last_entry_date
    }
    return render(request, "royaltyreports/partials/detail.html", context)
 


@permission_required('royaltyreports.add_report')
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
    return render(request, "royaltyreports/create-update.html", context) 

@permission_required('royaltyreports.change_report')
def report_update_view(request, id=None):
    obj = get_object_or_404(RoyaltyReport, id=id)
    form = ReportForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Report data saved.'
    if request.htmx:
        return render(request, "royaltyreports/partials/forms.html", context)
    return render(request, "royaltyreports/create-update.html", context) 


@permission_required('royaltyreports.change_report')
def report_hx_mark_complete(request, id=None):
    # if not request.htmx:
    #     raise Http404
    try:
        parent_obj = RoyaltyReport.objects.get(id=id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not found.")
    else:
        parent_obj.status = 'c'
        parent_obj.save()
        children = Event.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for event in children:
            event.status = 'c'
            event.royalty_report = parent_obj
            event.save()
            customers = EventCustomer.objects.filter(event=event.id)
            for each in customers:
                each.status = 'c'
                each.save()
        success_url = reverse('royalty:list')
        # if request.htmx:
        #     headers = {
        #         "HX-Redirect": success_url
        #     }
        #     return HttpResponse('Success', headers=headers)
        return redirect(success_url)


@permission_required('royaltyreports.change_report')
def report_hx_mark_pending(request, id=None):
    # if not request.htmx:
    #     raise Http404
    try:
        parent_obj = RoyaltyReport.objects.get(id=id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not found.")
    else:
        parent_obj.status = 'p'
        parent_obj.save()
        children = Event.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for event in children:
            event.status = 'p'
            event.save()
            customers = EventCustomer.objects.filter(event=event.id)
            for each in customers:
                each.status = 'p'
                each.save()
        success_url = reverse('royalty:list')
        # if request.htmx:
        #     headers = {
        #         "HX-Redirect": success_url
        #     }
        #     return HttpResponse('Success', headers=headers)
        return redirect(success_url)
